import os
from typing import List
from transactions_process_service.schemas.transaction import Transaction
from transactions_process_service.services.transaction_matcher import (
    TransactionMathcher,
)
from transactions_process_service.services.excel_creator import ExcelController
from tests.mocks.excel_creator.mock_transactions_and_matches import mock_data
    

def test_create_transaction_excel():
    workbook_name = "tests/output_tests_data/transactions_output.xlsx"
    bank_name = "Bank"
    system_name = "PharmBills System"

    excel_creator = ExcelController()
    excel_creator.create_transaction_excel(
        mock_data, workbook_name, bank_name, system_name
    )
    assert os.path.exists(workbook_name), "Excel file was not created"
