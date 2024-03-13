from transactions_process_service.schemas.transaction import Transaction
from transactions_process_service.services.parsers.system_parsers.system_parser import (
    PharmBillsParser,
)
from datetime import datetime


def test_parse_system_file():
    file_path = "tests/data/bankst.xls"
    first_transaction = Transaction(
        date=datetime(2023, 10, 1, 0, 0),
        description="gnss wire",
        amount=-37438.65,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
    )
    parser = PharmBillsParser()

    transactions = parser.parse_transactions(file_path)
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
