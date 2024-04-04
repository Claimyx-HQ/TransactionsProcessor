import logging
from typing import List
from fastapi import APIRouter, HTTPException, Response, UploadFile, status
from transactions_process_service.schemas.transaction import Transaction
from transactions_process_service.api.custom_exceptions import ParserMismatchException
from transactions_process_service.services.email_sender import send_error_email_with_uploadfiles
from transactions_process_service.services.parsers.parser_exceptions import CorrectParserNotFound
from transactions_process_service.services.transaction_matcher import TransactionMatcher
from transactions_process_service.services.parsers.file_parser import FileParser
from transactions_process_service.services.parsers.find_correct_parser import FindCorrectParser
from transactions_process_service.services.excel_creation.excel_controller import ExcelController
from transactions_process_service.services.parsers.system_parsers.system_parser import \
    PharmBillsParser


router = APIRouter()
@router.post("/process", summary="Process transactions")
async def process_transactions(system_file: UploadFile, bank_files: List[UploadFile]):
    try:
        logger = logging.getLogger(__name__)
        logger.info("In Process Transactions")
        # Initialization
        bank_detector = FindCorrectParser()
        transaction_matcher = TransactionMatcher()
        system_parser = PharmBillsParser()
        excel_controller = ExcelController()
        bank_name = "Bank"
        system_name = "PharmBills System"
        all_files = bank_files + [system_file]
        logger.info(f"Detected files: {all_files}")
        try:
            parser = verify_and_get_parser(bank_files, bank_detector)
            logger.info(f"Detected parser: {parser}")
            bank_parser = parser()
        except ParserMismatchException as e:
            raise ParserMismatchException(message=e)

        # Process transactions
        all_bank_transactions, system_transactions = process_all_transactions(
            bank_files, system_file, bank_parser, system_parser
        )
        logger.info(f"{len(all_bank_transactions)} bank_transactions")
        logger.info(f"{len(system_transactions)} system_transactions")
        # Find matches
        data = find_matches(
            all_bank_transactions, system_transactions, transaction_matcher
        )

        # Create and return Excel file
        return generate_excel_response(data, excel_controller, bank_name, system_name)

    except ParserMismatchException as e:
        logger.exception(e)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except CorrectParserNotFound as e:
        logger.exception(e)
        send_error_email_with_uploadfiles("Parser not found", str(e), all_files)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(e)
        send_error_email_with_uploadfiles("Unexpected error", str(e), all_files)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def verify_and_get_parser(bank_files: List[UploadFile], bank_detector: FindCorrectParser):
    logger = logging.getLogger(__name__)
    parser_types = [
        type(bank_detector.find_parser(file)) for file in bank_files
    ]
    logger.info(f"Parser types: {parser_types}")
    set_parser_types = set(parser_types)
    if len(set_parser_types) > 1:
        raise ParserMismatchException(parser_types)

    return parser_types[0]


def process_all_transactions(bank_files: List[UploadFile], system_file: UploadFile, bank_parser: FileParser, system_parser: FileParser):
    all_bank_transactions = [
        transaction
        for file in bank_files
        for transaction in bank_parser.parse_transactions(file)
    ]
    system_transactions = system_parser.parse_transactions(system_file)
    return all_bank_transactions, system_transactions


def find_matches(all_bank_transactions: List[Transaction], system_transactions: List[Transaction], transaction_matcher: TransactionMatcher):
    logger = logging.getLogger(__name__)
    perfect_matches, unmatched_bank_amounts, unmatched_system_amounts = (
        transaction_matcher.find_matched_unmatched(
            [t.amount for t in all_bank_transactions],
            [t.amount for t in system_transactions],
        )
    )
    zero_and_negative_system_amounts = [
        amount for amount in unmatched_system_amounts if amount <= 0
    ]
    unmatched_system_amounts = [
        amount for amount in unmatched_system_amounts if amount > 0
    ]
    matches, unmatched_bank_amounts, unmatched_system_amounts = (
        transaction_matcher.find_reconciling_matches(
            unmatched_bank_amounts, unmatched_system_amounts
        )
    )
    unmatched_system_amounts.extend(zero_and_negative_system_amounts)
    logger.info(f"""
        "transactions": "system": {len(system_transactions)}, "bank": {len(all_bank_transactions)},
        "matches": 
            "one_to_one": {len(perfect_matches)},
            "multi_to_one": {len(matches)},
            "unmatched_system": {len(unmatched_system_amounts)},
            "unmatched_bank": {len(unmatched_bank_amounts)},
        ,
    """)
    return {
        "transactions": {"system": system_transactions, "bank": all_bank_transactions},
        "matches": {
            "one_to_one": perfect_matches,
            "multi_to_one": matches,
            "unmatched_system": unmatched_system_amounts,
            "unmatched_bank": unmatched_bank_amounts,
        },
    }


def generate_excel_response(
    data,
    excel_controller: ExcelController,
    bank_name="Bank",
    system_name="PharmBills System",
):
    output = excel_controller.create_transaction_excel(
        data, None, bank_name, system_name
    )
    if output is None:
        return Response(
            content="No matches found", status_code=status.HTTP_404_NOT_FOUND
        )
    headers = {
        "Content-Disposition": "attachment; filename=result.xlsx",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }
    return Response(content=output.read(), headers=headers)
