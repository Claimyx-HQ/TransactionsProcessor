import os
from typing import List
from tests.mocks.excel_creator.mock_transactions_and_matches import mock_data
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.excel.excel_controller import ExcelController
from datetime import datetime


def test_create_transaction_excel():  # TODO: Correct the mock data, create_transaction_excel() works with Transaction model and not dict
    workbook_name = "tests/output_tests_data/transactions_output.xlsx"
    bank_name = "Bank"
    system_name = "PharmBills System"

    excel_creator = ExcelController()
    mock_data["transactions"]["system"] = [
        Transaction(
            uuid=transaction["uuid"],
            date=datetime.strptime(transaction["date"], "%m-%d-%Y"),
            description=transaction["description"],
            amount=transaction["amount"],
            batch_number=transaction["batch_number"],
        )
        for transaction in mock_data["transactions"]["system"]
    ]
    mock_data["transactions"]["bank"] = [
        Transaction(
            uuid=transaction["uuid"],
            date=datetime.strptime(transaction["date"], "%m-%d-%Y"),
            description=transaction["description"],
            amount=transaction["amount"],
        )
        for transaction in mock_data["transactions"]["bank"]
    ]
    excel_creator.create_transaction_excel(
        mock_data, workbook_name, bank_name, system_name
    )
    assert os.path.exists(workbook_name), "Excel file was not created"
