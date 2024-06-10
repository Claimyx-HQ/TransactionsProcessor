import os
from typing import List
from tests.mocks.excel_creator.mock_transactions_and_matches import mock_data
from transactions_processor.services.excel.excel_controller import ExcelController
    

def test_create_transaction_excel(): # TODO: Correct the mock data, create_transaction_excel() works with Transaction model and not dict 
    workbook_name = "tests/output_tests_data/transactions_output.xlsx"
    bank_name = "Bank"
    system_name = "PharmBills System"

    excel_creator = ExcelController()
    excel_creator.create_transaction_excel(
        mock_data, workbook_name, bank_name, system_name
    )
    assert os.path.exists(workbook_name), "Excel file was not created"
