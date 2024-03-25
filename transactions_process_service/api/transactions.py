import time
from typing import Any, List
from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from transactions_process_service.services.excel_creation.excel_controller import ExcelController
from transactions_process_service.services.parsers.bank_parsers.forbright_bank_parser import (
    ForbrightBankParser,
)
from transactions_process_service.services.parsers.find_correct_parser import (
    FindCorrectParser,
)
from transactions_process_service.services.parsers.system_parsers.system_parser import (
    PharmBillsParser,
)

from transactions_process_service.services.transaction_matcher import (
    TransactionMathcher,
)


router = APIRouter()
some_file_path = "tests/data/bankst.xls"


@router.post(
    "/process",
    # response_model=List[BuyBoxData],
)
async def process_transactions(system_file: UploadFile, bank_file: UploadFile):
    try:
        bank_name = "Bank"
        system_name = "PharmBills System"
        bank_detector = FindCorrectParser()
        transaction_matcher = TransactionMathcher()
        # bank_parser = ForbrightBankParser()
        system_parser = PharmBillsParser()
        excel_controller = ExcelController()

        start = time.time()

        bank_parser = bank_detector.find_parser(bank_file.file)

        bank_transactions = bank_parser.parse_transactions(bank_file.file)
        system_transactions = system_parser.parse_transactions(system_file.file)

        end = time.time()
        print(f"Time taken to parse transactions: {end - start}")
        print(f"transactions: {bank_transactions} ")

        start = time.time()

        (
            perfect_matches,
            unmatched_bank_amounts,
            unmatched_system_amounts,
        ) = transaction_matcher.find_matched_unmatched(
            [t.amount for t in bank_transactions],
            [t.amount for t in system_transactions],
        )

        end = time.time()
        print(f"Time taken to find matched unmatched: {end - start}")

        # remove all amounts zero or less in unmatched_system_amounts
        unmatched_system_amounts = list(
            filter(lambda x: x > 0, unmatched_system_amounts)
        )

        start = time.time()

        (
            matches,
            unmatched_bank_amounts,
            unmatched_system_amounts,
        ) = transaction_matcher.find_reconciling_matches(
            unmatched_bank_amounts, unmatched_system_amounts
        )

        end = time.time()
        print(f"Time taken to find matches: {end - start}")

        data = {
            "transactions": {
                "system": system_transactions,
                "bank": bank_transactions,
            },
            "matches": {
                "one_to_one": perfect_matches,
                "multi_to_one": matches,
                "unmatched_system": unmatched_system_amounts,
                "unmatched_bank": unmatched_bank_amounts,
            },
        }

        start = time.time()

        output = excel_controller.create_transaction_excel(
            data, None, bank_name, system_name
        )

        end = time.time()
        print(f"Time taken to create excel: {end - start}")

        if output is None:
            return Response(
                content="No matches found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        headers = {
            "Content-Disposition": f"attachment; filename=result.xlsx",
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }

        return Response(content=output.read(), headers=headers)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
