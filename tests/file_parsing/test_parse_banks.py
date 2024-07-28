from datetime import datetime
import logging

# conftest.py or your specific test file
import pytest
import pandas as pd
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.bank_parsers.amalgamated_bank_parser import AmalgamatedBankParser
from transactions_processor.services.parsers.bank_parsers.bank_feeds_parser import (
    BankFeedsParser,
)
from transactions_processor.services.parsers.bank_parsers.bhi_bank_parser import (
    BHIBankParser,
)
from transactions_processor.services.parsers.bank_parsers.cfg_bank_parser import CfgBankParser
from transactions_processor.services.parsers.bank_parsers.cibc_bank_parser import (
    CIBCBankParser,
)
from transactions_processor.services.parsers.bank_parsers.citizens_bank_parser import CitizensBankParser
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
from transactions_processor.services.parsers.bank_parsers.key_bank_parser import KeyBankParser
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
from transactions_processor.services.parsers.bank_parsers.regions_bank_parser import RegionsBankParser
from transactions_processor.services.parsers.bank_parsers.servis1st_bank_parser import (
    Servis1stBankParser,
)
from transactions_processor.services.parsers.bank_parsers.the_berkshire_bank_parser import TheBerkshireBankParser
from transactions_processor.services.parsers.bank_parsers.united_bank_parser import (
    UnitedBankParser,
)

from transactions_processor.services.parsers.bank_parsers.vista_bank_parser import VistaBankParser


from transactions_processor.services.parsers.bank_parsers.vera_bank_parser import VeraBankParser

from transactions_processor.services.parsers.bank_parsers.valley_bank_parser import ValleyBankParser

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
    file_path = "tests/data/banks/forbright/forbright_bank_4.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 3, 4, 0, 0),
        description="' Cash Mgmt Trsfr Cr",
        amount=7903.0,
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
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 2, 2, 0, 0),
        description="NOVITAS SOLUTION HCCLAIMPMT",
        amount=18152.75,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
    )
    parser = UnitedBankParser()

    transactions = parser.parse_transactions(file)
    # Assuming `transactions` is a list of transaction objects or dictionaries you want to log
    formatted_transactions = " \n".join(str(t) for t in transactions)
    logger.info(f"\nFormatted Transactions:\n{formatted_transactions}\n")
    parsed_transaction = transactions[0]

    _check_the_test(first_transaction, parsed_transaction)
    file.close()


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

def test_parse_key_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/key/key_bank_1.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 5, 1, 0, 0),
        description="Key Capture Deposit",
        amount=46079.17,
        uuid="70b4046c-f1f9-4d17-83a7-eea2f14fa4a5",
    )
    parser = KeyBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()

def test_parse_citizens_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/citizens/citizens_bank_2.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 3, 1, 0, 0),
        description="Square Inc 240301P2 240301 L21564304743",
        amount=384.85,
        uuid="2ef3f67e-583e-40f4-bb19-f76dcbaff0c7",
    )
    parser = CitizensBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()



def test_parse_vista_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/vista/vista_bank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 7, 0, 0),
        description="HEALTH HUMAN SVC/HCCLAIMPMT",
        amount=26063.85,
        uuid="7302f8aa-fcf2-4f34-b37a-b10d3495c05e",
    )
    parser = VistaBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()

def test_parse_vera_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/vera/vera_bank_after_ocr.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 4, 0, 0),
        description="HENDERSON HEALTH/SETTLEMENT 000021044683986 GLOBAL HEALTHCARE FISC",
        amount=2324.0,
        uuid="17d9d2d9-3c0e-49cf-8e1d-21500ffc3ecd",
    )
    parser = VeraBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_valley_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/valley/valley_bank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 3, 0, 0),
        description="ACH CREDIT",
        amount=3088.0,
        uuid="c8049255-7a0c-4618-8798-6c749e1e0030",
    )
    parser = ValleyBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()

def test_parse_amalgamated_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/amalgamated/amalgamated_bank_after_ocr.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 5, 1, 0, 0),
        description="BANKCARD/MTOT DEP 518993320356520",
        amount=444.14,
        uuid="cc0629b4-375d-4314-a813-6945228194b4",
    )
    parser = AmalgamatedBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()
    
def test_parse_the_berkshire_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/the_berkshire/the_berkshire_after_ocr.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 5, 6, 0, 0),
        description="FAC 3207 NDC SWEEP 1541194122 05/06/24 TRACE #-211274453204553",
        amount=32421.42,
        uuid="e04d0f6c-61df-4ba7-bd27-dff82084ba7d",
    )

    parser = TheBerkshireBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()

def test_parse_cfg_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/cfg/CFG_bank_1.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 5, 1, 0, 0),
        description="Wire Credit WYTHE VA OPCO LLC Wires",
        amount=174842.39,
        uuid="b1ab9a34-7ed2-44b3-b328-f2dd12fe86d8",
    )
    parser = CfgBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()

def test_parse_regions_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/regions/regions_bank_1.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 3, 1, 0, 0),
        description="NDC SweepFac C893  Silver Stream",
        amount=8557.0,
        uuid="94769be0-2915-434f-b211-ae074c1cc1f4",
    )
    parser = RegionsBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()

