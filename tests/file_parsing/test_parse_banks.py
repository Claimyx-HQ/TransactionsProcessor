from datetime import datetime
import logging

# conftest.py or your specific test file
import pytest
import pandas as pd
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.bank_parsers.bank_feeds_parser import (
    BankFeedsParser,
)
from transactions_processor.services.parsers.bank_parsers.bhi_bank_parser import (
    BHIBankParser,
)
from transactions_processor.services.parsers.bank_parsers.cibc_bank_parser import (
    CIBCBankParser,
)
from transactions_processor.services.parsers.bank_parsers.connect_one_bank_parser import (
    ConnectOneBankParser,
)
from transactions_processor.services.parsers.bank_parsers.daca_bank_parser import (
    DACABankParser,
)
from transactions_processor.services.parsers.bank_parsers.flagstar_bank_parser import (
    FlagstarBankParser,
)
from transactions_processor.services.parsers.bank_parsers.forbright_bank_parser import (
    ForbrightBankParser,
)
from transactions_processor.services.parsers.bank_parsers.huntington_bank_parser import (
    HuntingtonBankParser,
)
from transactions_processor.services.parsers.bank_parsers.metropolitan_bank_parser import (
    MetropolitanBankParser,
)
from transactions_processor.services.parsers.bank_parsers.midwest_bank_parser import (
    MidwestBankParser,
)
from transactions_processor.services.parsers.bank_parsers.pnc_bank_parser import (
    PNCBankParser,
)
from transactions_processor.services.parsers.bank_parsers.popular_bank_parser import (
    PopularBankParser,
)
from transactions_processor.services.parsers.bank_parsers.servis1st_bank_parser import (
    Servis1stBankParser,
)
from transactions_processor.services.parsers.bank_parsers.united_bank_parser import (
    UnitedBankParser,
)
from transactions_processor.services.parsers.bank_parsers.webster_bank_parser import (
    WebsterBankParser,
)
from transactions_processor.services.parsers.bank_parsers.wells_fargo_bank_parser import (
    WellsFargoBankParser,
)


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
    file_path = "tests/data/banks/forbright/forbright_bank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2023, 10, 2, 0, 0),
        description="Preauthorized Credit",
        amount=3766.0,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
    )
    parser = ForbrightBankParser()

    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]

    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_united_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/united/united_bank.pdf"
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
    file_path = "tests/data/banks/flagstar/flagstar_bank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 3, 4, 0, 0),
        description="ACH DEPOSITck/ref no.4301137",
        amount=3000.0,
        uuid="957be6d2-2419-4443-90a2-213110210e9d",
    )
    parser = FlagstarBankParser()

    transactions = parser.parse_transactions(file)
    # Assuming `transactions` is a list of transaction objects or dictionaries you want to log
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]

    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_connect_one_bank():

    # Be cautious with these settings for very large DataFrames

    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/connect_one/connect_one_bank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 2, 8, 0, 0),
        description="Maintenance Fee Rfnd",
        amount=100.59,
        uuid="dc924399-5628-4884-8180-7a3eb6d52a25",
    )
    parser = ConnectOneBankParser()

    transactions = parser.parse_transactions(file)
    # Assuming `transactions` is a list of transaction objects or dictionaries you want to log
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]

    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_servis1st_bank():

    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/servis1st/servis1st_bank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 3, 1, 0, 0),
        description="From DDA 1110372735,To DDA 111",
        amount=190000.0,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = Servis1stBankParser()

    transactions = parser.parse_transactions(file)
    # Assuming `transactions` is a list of transaction objects or dictionaries you want to log
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_bank_feeds():

    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/bank_feeds/bank_feeds.csv"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 5, 28, 0, 0),
        description="ZBA CREDIT TRANSFER FR 0310317929",
        amount=688.09,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = BankFeedsParser()

    transactions = parser.parse_transactions(file)
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_webster_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/webster/WebsterBank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 4, 1, 0, 0),
        description="FUND FROM DDA",
        amount=9088.48,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = WebsterBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_pnc_bank():

    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/pnc/pnc84.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 5, 24, 0, 0),
        description="CORPORATE ACH 517927880310164",
        amount=1745.0,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = PNCBankParser()

    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_daca_bank():

    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/daca/DACA.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 5, 6, 0, 0),
        description="AETNA AS01PREAUTHORIZED ACH",
        amount=5614.46,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = DACABankParser()

    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_popular_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/popular/Popular.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 4, 1, 0, 0),
        description="Preauthorized Credit",
        amount=1399.24,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = PopularBankParser()

    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_metropolitan_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/metropolitan/Metropolitan.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 4, 1, 0, 0),
        description="TRANSFER FROM 03-99021949",
        amount=1255.62,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = MetropolitanBankParser()

    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


# TODO: need to finish this bank
def test_parse_wells_fargo_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/wells_fargo/WellsFargo.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 5, 1, 0, 0),
        description="Bankcard Mtot Dep 230430 518993320356330 North Campus Rehab and",
        amount=50.00,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = WellsFargoBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_huntington_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/huntington/Huntington.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 4, 2, 0, 0),
        description="ECHO-AMERIHEALTH HCCLAIMPMT 240402 264320480 TRN*1*1131116478*1341858379\\",
        amount=333678.01,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = HuntingtonBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_cibc_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/cibc/CIBC.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 4, 1, 0, 0),
        description="Preauthorized Credit",
        amount=5664.32,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = CIBCBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_bhi_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/bhi/BHI.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 5, 2, 0, 0),
        description="INCOMING ACH CREDIT",
        amount=12151.13,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = BHIBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_midwest_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/midwest/Midwest.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 4, 1, 0, 0),
        description="' Preauthorized Credit",
        amount=276.13,
        uuid="4f9d028b-10db-4a1b-be79-09b75b482e77",
    )
    parser = MidwestBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()
