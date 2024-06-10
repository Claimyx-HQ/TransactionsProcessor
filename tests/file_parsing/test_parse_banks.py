from datetime import datetime
import logging

# conftest.py or your specific test file
import pytest
import pandas as pd
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.bank_parsers.connect_one_bank_parser import ConnectOneBankParser
from transactions_processor.services.parsers.bank_parsers.flagstar_bank_parser import FlagstarBankParser
from transactions_processor.services.parsers.bank_parsers.forbright_bank_parser import ForbrightBankParser
from transactions_processor.services.parsers.bank_parsers.servis1st_bank_parser import Servis1stBankParser
from transactions_processor.services.parsers.bank_parsers.united_bank_parser import UnitedBankParser


@pytest.fixture(autouse=True)
def pandas_display_settings():
    pd.set_option("display.max_rows", None)  # Display all rows
    pd.set_option("display.max_columns", None)  # Display all columns
    pd.set_option("display.max_colwidth", None)  # Display full content of each column
    yield


def _check_the_test(first_transaction, parsed_transaction):
    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount


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
    print(f'transactions: {transactions}')
    parsed_transaction = transactions[0]

    _check_the_test(first_transaction, parsed_transaction)


def test_parse_united_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/united_bank.pdf"
    first_transaction = Transaction(
        date=datetime(2024, 2, 2, 0, 0),
        description="NOVITAS SOLUTION HCCLAIMPMT",
        amount=18152.75,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
    )
    parser = UnitedBankParser()

    transactions = parser.parse_transactions(file_path)
    # Assuming `transactions` is a list of transaction objects or dictionaries you want to log
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]

    _check_the_test(first_transaction, parsed_transaction)


def test_parse_flagstar_bank():

    # Be cautious with these settings for very large DataFrames

    logger = logging.getLogger(__name__)
    file_path = "tests/data/flagstar/flagstar_bank.pdf"
    first_transaction = Transaction(
        date=datetime(2024, 3, 4, 0, 0),
        description='ACH DEPOSITck/ref no.4301137',
        amount=3000.0,
        uuid='957be6d2-2419-4443-90a2-213110210e9d', 
    )
    parser = FlagstarBankParser()

    transactions = parser.parse_transactions(file_path)
    # Assuming `transactions` is a list of transaction objects or dictionaries you want to log
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]

    _check_the_test(first_transaction, parsed_transaction)


def test_parse_connect_one_bank():

    # Be cautious with these settings for very large DataFrames

    logger = logging.getLogger(__name__)
    file_path = "tests/data/connect_one/connect_one_bank.pdf"
    first_transaction = Transaction(
        date=datetime(2024, 2, 8, 0, 0),
        description="Maintenance Fee Rfnd",
        amount=100.59,
        uuid="dc924399-5628-4884-8180-7a3eb6d52a25",
    )
    parser = ConnectOneBankParser()

    transactions = parser.parse_transactions(file_path)
    # Assuming `transactions` is a list of transaction objects or dictionaries you want to log
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]

    _check_the_test(first_transaction, parsed_transaction)


def test_parse_servis1st_bank():

    logger = logging.getLogger(__name__)
    file_path = "tests/data/servis1st/servis1st_bank.pdf"
    first_transaction = Transaction(
        date=datetime(2024, 3, 1, 0, 0),
        description='From DDA 1110372735,To DDA 111',
        amount=190000.0,
        uuid='4f9d028b-10db-4a1b-be79-09b75b482e77',
    )
    parser = Servis1stBankParser()

    transactions = parser.parse_transactions(file_path)
    # Assuming `transactions` is a list of transaction objects or dictionaries you want to log
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)

