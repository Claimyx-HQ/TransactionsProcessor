import io
import os
from tests.mocks.excel_creator.mock_transactions_and_matches import mock_data
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.excel.excel_controller import ExcelController
from datetime import datetime

from transactions_processor.services.parsers.bank_parsers.bankwell_bank_parser import (
    BankWellBankParser,
)
from transactions_processor.services.parsers.system_parsers.pcc.pcc_parser import (
    PCCParser,
)
from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)
from transactions_processor.services.reconciliation.transactions_matcher import (
    TransactionsMatcher,
)


def test_create_transaction_excel2():  # TODO: Correct the mock data, create_transaction_excel() works with Transaction model and not dict
    workbook_name = "tests/output_tests_data/transactions_output.xlsx"
    bank_name = "Bank"
    system_name = "PharmBills System"
    raw_system_file = "tests/data/excel_creation/PCC report.pdf"
    with open(raw_system_file, "rb") as f:
        system_file = io.BytesIO(f.read())
    system_parser: TransactionsParser = PCCParser()
    system_transactions = system_parser.parse_transactions(
        system_file,
        raw_system_file.split("/")[-1],
        "",
    )
    bank_files_paths = [
        "tests/data/excel_creation/775 Dep.pdf",
        "tests/data/excel_creation/775 Gov.pdf",
        "tests/data/excel_creation/775 Ope.pdf",
        "tests/data/excel_creation/775 Pay.pdf",
    ]
    bank_transactions = []
    for file_path in bank_files_paths:
        with open(file_path, "rb") as f:
            file = io.BytesIO(f.read())
        bank_file_key = ""
        bank_file_name = file_path.split("/")[-1]
        bank_file = file
        bank_parser: TransactionsParser = BankWellBankParser()
        parsed_bank_transactions = bank_parser.parse_transactions(
            bank_file, bank_file_name, bank_file_key
        )
        bank_transactions.extend(parsed_bank_transactions)

    data = {}
    transaction_matcher = TransactionsMatcher()
    data["transactions"] = {}
    data["transactions"]["system"] = system_transactions
    data["transactions"]["bank"] = bank_transactions

    matched_transactions = transaction_matcher.find_one_to_one_matches(
        bank_transactions, system_transactions
    )

    multi_matches = transaction_matcher.find_one_to_many_matches(
        matched_transactions.unmatched_bank,
        matched_transactions.unmatched_system,
    )
    mock_data = {
        "transactions": {"system": system_transactions, "bank": bank_transactions},
        "matches": {
            "one_to_one": matched_transactions.matched,
            "many_to_many": multi_matches.matched,
            "unmatched_system": multi_matches.unmatched_system,
            "unmatched_bank": multi_matches.unmatched_bank,
            "excluded": {
                "system": {"test": [multi_matches.matched[0][0][0]]},
                # "bank": {"test": ["move money"]},
            },
        },
    }
    excel_creator = ExcelController()

    excel_creator.create_transaction_excel(
        mock_data, workbook_name, bank_name, system_name
    )
    assert os.path.exists(workbook_name), "Excel file was not created"
