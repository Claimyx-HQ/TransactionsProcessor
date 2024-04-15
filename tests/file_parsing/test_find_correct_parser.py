import logging
from datetime import datetime

import pytest
from transactions_process_service.schemas.transaction import Transaction
from transactions_process_service.services.parsers.bank_parsers.connect_one_bank_parser import ConnectOneBankParser
from transactions_process_service.services.parsers.bank_parsers.flagstar_bank_parser import FlagstarBankParser
from transactions_process_service.services.parsers.bank_parsers.united_bank_parser import (
    UnitedBankParser,
)
from transactions_process_service.services.parsers.bank_parsers.forbright_bank_parser import (
    ForbrightBankParser,
)
from transactions_process_service.services.parsers.find_correct_parser import (
    FindCorrectParser,
)
from transactions_process_service.services.parsers.parser_exceptions import (
    CorrectParserNotFound,
)


def test_find_correct_parser_for_unknown_PDF():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/Mifrat_500e_v2.pdf"
    with pytest.raises(CorrectParserNotFound):
        parser = FindCorrectParser()
        found_parser = parser.find_parser(file_path)


def test_find_correct_parser_for_united_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/united_bank.pdf"
    correct_parser = UnitedBankParser
    first_transaction = Transaction(
        date=datetime(2024, 2, 2, 0, 0),
        description="NOVITAS SOLUTION HCCLAIMPMT",
        amount=18152.75,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
    )

    parser = FindCorrectParser()
    found_parser = parser.find_parser(file_path)
    transactions = found_parser.parse_transactions(file_path)
    # Assuming `transactions` is a list of transaction objects or dictionaries you want to log
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]

    assert isinstance(found_parser, correct_parser)
    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount


def test_find_correct_parser_for_forbright_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/forbright_bank.pdf"
    correct_parser = ForbrightBankParser
    first_transaction = Transaction(
        date=datetime(2023, 10, 2, 0, 0),
        description="Preauthorized Credit",
        amount=3766.0,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
    )

    parser = FindCorrectParser()
    found_parser = parser.find_parser(file_path)
    transactions = found_parser.parse_transactions(file_path)
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]

    assert isinstance(found_parser, correct_parser)
    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount

def test_find_correct_parser_for_flagstar_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/flagstar/flagstar_bank.pdf"
    correct_parser = FlagstarBankParser
    first_transaction = Transaction(
        date=datetime(2024, 2, 1, 0, 0),
        description="ACH DEPOSITck/ref no.1087988",
        amount=15671.56,
        uuid="4e73dbc8-297c-4270-acf4-ea41acfa41ee",
    )

    parser = FindCorrectParser()
    found_parser = parser.find_parser(file_path)
    transactions = found_parser.parse_transactions(file_path)
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]

    assert isinstance(found_parser, correct_parser)
    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount

def test_find_correct_parser_for_connect_one_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/connect_one/connect_one_bank.pdf"
    correct_parser = ConnectOneBankParser
    first_transaction = Transaction(
        date=datetime(2024, 2, 8, 0, 0),
        description="Maintenance Fee Rfnd",
        amount=100.59,
        uuid="dc924399-5628-4884-8180-7a3eb6d52a25",
    )

    parser = FindCorrectParser()
    found_parser = parser.find_parser(file_path)
    transactions = found_parser.parse_transactions(file_path)
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]

    assert isinstance(found_parser, correct_parser)
    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
