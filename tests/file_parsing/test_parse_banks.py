from datetime import datetime
from transactions_process_service.schemas.transaction import Transaction
from transactions_process_service.services.parsers.bank_parsers.united_bank_parser import (
    UnitedBankParser,
)

from transactions_process_service.services.parsers.bank_parsers.forbright_bank_parser import (
    ForbrightBankParser,
)


def test_parse_forbright_bank():
    file_path = "tests/data/forbright_bank.pdf"
    first_transaction = Transaction(
        date=datetime(2023, 10, 2, 0, 0),
        description="Preauthorized Credit",
        amount=3766.0,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
    )
    parser = ForbrightBankParser()

    transactions = parser.parse_transactions(file_path)
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount


def test_parse_united_bank():
    file_path = "tests/data/united_bank.pdf"
    first_transaction = Transaction(
        date=datetime(2024, 2, 2, 0, 0),
        description="NOVITAS SOLUTION HCCLAIMPMT",
        amount=18152.75,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
    )
    parser = UnitedBankParser()

    transactions = parser.parse_transactions(file_path)
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
