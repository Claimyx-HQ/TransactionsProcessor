import time
from typing import Any, List
from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from transactions_process_service.api.custom_exceptions import ParserMismatchException
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
async def process_transactions(system_file: UploadFile, bank_files: List[UploadFile]):
    try:
        bank_name = "Bank"
        system_name = "PharmBills System"
        bank_detector = FindCorrectParser()
        transaction_matcher = TransactionMathcher()
        system_parser = PharmBillsParser()
        excel_controller = ExcelController()

        start = time.time()
        # Check if all files have the same parser
        parser_types = []
        for bank_file in bank_files:
            parser = bank_detector.find_parser(bank_file.file)
            if parser is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f"Parser not found for one of the files: {bank_file.filename}"
                )
            parser_types.append(type(parser).__name__)
        if len(set(parser_types)) > 1:
            raise ParserMismatchException(parser_types)
        
        all_bank_transactions = []
        bank_parser = bank_detector.find_parser(bank_files[0].file) # Because all files have the same parser
        for bank_file in bank_files:
            from_file_bank_transactions = bank_parser.parse_transactions(bank_file.file)
            all_bank_transactions.extend(from_file_bank_transactions)

        system_transactions = system_parser.parse_transactions(system_file.file)

        end = time.time()
        print(f"Time taken to parse transactions: {end - start}")
        print(f"transactions: {all_bank_transactions} ")

        start = time.time()

        (
            perfect_matches,
            unmatched_bank_amounts,
            unmatched_system_amounts,
        ) = transaction_matcher.find_matched_unmatched(
            [t.amount for t in all_bank_transactions],
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
                "bank": all_bank_transactions,
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
    
    except ParserMismatchException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
