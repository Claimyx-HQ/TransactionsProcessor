from datetime import datetime
import logging

# conftest.py or your specific test file
import pytest
import pandas as pd
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.bank_parsers.amalgamated_bank_parser import (
    AmalgamatedBankParser,
)
from transactions_processor.services.parsers.bank_parsers.bank_feeds_parser import (
    BankFeedsParser,
)
from transactions_processor.services.parsers.bank_parsers.bank_of_america_merrill_lynch_parser import (
    BankOfAmericaMerrillLynchParser,
)
from transactions_processor.services.parsers.bank_parsers.bank_of_texas_parser import (
    BankOfTexasParser,
)
from transactions_processor.services.parsers.bank_parsers.bankwell_bank_parser import (
    BankWellBankParser,
)
from transactions_processor.services.parsers.bank_parsers.bhi_bank_parser import (
    BHIBankParser,
)
from transactions_processor.services.parsers.bank_parsers.cadence_bank_parser import (
    CadenceBankParser,
)
from transactions_processor.services.parsers.bank_parsers.capital_one_bank_parser import (
    CapitalOneBankParser,
)
from transactions_processor.services.parsers.bank_parsers.cfg_bank_parser import (
    CfgBankParser,
)
from transactions_processor.services.parsers.bank_parsers.chase_bank_parser import (
    ChaseBankParser,
)
from transactions_processor.services.parsers.bank_parsers.cibc_bank_parser import (
    CIBCBankParser,
)
from transactions_processor.services.parsers.bank_parsers.citizens_bank_parser import (
    CitizensBankParser,
)
from transactions_processor.services.parsers.bank_parsers.connect_one_bank_parser import (
    ConnectOneBankParser,
)
from transactions_processor.services.parsers.bank_parsers.customers_bank_parser import (
    CustomersBankParser,
)
from transactions_processor.services.parsers.bank_parsers.daca_bank_parser import (
    DACABankParser,
)
from transactions_processor.services.parsers.bank_parsers.first_financial_bank_parser import (
    FirstFinancialBankParser,
)
from transactions_processor.services.parsers.bank_parsers.first_united_bank_parser import (
    FirstUnitedBankParser,
)
from transactions_processor.services.parsers.bank_parsers.flagstar_bank_parser import (
    FlagstarBankParser,
)
from transactions_processor.services.parsers.bank_parsers.forbright_bank_parser import (
    ForbrightBankParser,
)
from transactions_processor.services.parsers.bank_parsers.hancock_whitney_bank_parser import (
    HancockWhitneyBankParser,
)
from transactions_processor.services.parsers.bank_parsers.huntington_bank_parser import (
    HuntingtonBankParser,
)
from transactions_processor.services.parsers.bank_parsers.key_bank_parser import (
    KeyBankParser,
)
from transactions_processor.services.parsers.bank_parsers.legend_bank_parser import (
    LegendBankParser,
)
from transactions_processor.services.parsers.bank_parsers.metropolitan_bank_parser import (
    MetropolitanBankParser,
)
from transactions_processor.services.parsers.bank_parsers.midwest_bank_parser import (
    MidwestBankParser,
)
from transactions_processor.services.parsers.bank_parsers.midfirst_bank_parser import (
    MidFirstBankParser,
)
from transactions_processor.services.parsers.bank_parsers.old_national_bank_parser import (
    OldNationalBankParser,
)
from transactions_processor.services.parsers.bank_parsers.pnc_bank_parser import (
    PNCBankParser,
)
from transactions_processor.services.parsers.bank_parsers.popular_bank_parser import (
    PopularBankParser,
)
from transactions_processor.services.parsers.bank_parsers.regions_bank_parser import (
    RegionsBankParser,
)
from transactions_processor.services.parsers.bank_parsers.servis1st_bank_parser import (
    Servis1stBankParser,
)
from transactions_processor.services.parsers.bank_parsers.simmons_bank_parser import (
    SimmonsBankParser,
)
from transactions_processor.services.parsers.bank_parsers.state_bank_parser import (
    StateBankParser,
)
from transactions_processor.services.parsers.bank_parsers.sunflower_bank_parser import (
    SunflowerBankParser,
)
from transactions_processor.services.parsers.bank_parsers.the_berkshire_bank_parser import (
    TheBerkshireBankParser,
)
from transactions_processor.services.parsers.bank_parsers.tomball_baylor_bank_parser import (
    TomballBaylorBankParser,
)
from transactions_processor.services.parsers.bank_parsers.truist_bank_parser import (
    TruistBankParser,
)
from transactions_processor.services.parsers.bank_parsers.united_bank_parser import (
    UnitedBankParser,
)

from transactions_processor.services.parsers.bank_parsers.vista_bank_parser import (
    VistaBankParser,
)


from transactions_processor.services.parsers.bank_parsers.vera_bank_parser import (
    VeraBankParser,
)

from transactions_processor.services.parsers.bank_parsers.valley_bank_parser import (
    ValleyBankParser,
)

from transactions_processor.services.parsers.bank_parsers.webster_bank_parser import (
    WebsterBankParser,
)
from transactions_processor.services.parsers.bank_parsers.wells_fargo_bank_parser import (
    WellsFargoBankParser,
)


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
        origin="forbright_bank_4.pdf",
    )
    parser = ForbrightBankParser()

    transactions = parser.parse_transactions(file, "forbright_bank_4.pdf")
    parsed_transaction = transactions[0]

    _check_the_test(first_transaction, parsed_transaction)
    assert first_transaction.origin == parsed_transaction.origin
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

    transactions = parser.parse_transactions(file, "bank_feeds.csv")
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


def test_parse_legend_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/legend/legend_bank_after_ocr.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 18, 0, 0),
        description="Tomball Rehab & Settlement 000021168080014",
        amount=813.06,
        uuid="92de6227-cec5-4227-93c7-a210c6c0b29f",
    )
    parser = LegendBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_midfirst_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/midfirst/midfirst_bank_after_ocr.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 12, 0, 0),
        description="#ACH Deposit",
        amount=3782.26,
        uuid="a92e70b9-35ce-47a1-a404-4e8287ae84b1",
    )
    parser = MidFirstBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_old_national_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/old_national/old_national_after_ocr.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 4, 0, 0),
        description="WISCONSIN PHYSIC HCCLAIMPMT",
        amount=16484.1,
        uuid="30f474dc-c364-4e2b-aa9f-936abcde00b5",
    )
    parser = OldNationalBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_simmons_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/simmons/simmons_bank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 3, 0, 0),
        description="HCCLAIMPMT HNB - ECHO",
        amount=2004.04,
        uuid="0b874abc-4858-4f49-bc5b-a10ff331a806",
    )
    parser = SimmonsBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_state_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/state/state_bank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 3, 0, 0),
        description="CLARKSVILLE NURS SETTLEMENT",
        amount=1160.5,
        uuid="ce5d4279-318c-4dbf-8b5b-b48996e02208",
    )
    parser = StateBankParser()
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


def test_parse_hancock_whitney_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/hancock_whitney/hancock_whitney_after_ocr.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 13, 0, 0),
        description="PAYABLES CURO HEALTH SERV",
        amount=549.44,
        uuid="e3b15eb9-48b2-4728-9ec3-ed1bc99a8b44",
    )
    parser = HancockWhitneyBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_first_united_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/first_united/first_united_bank_after_ocr.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 3, 0, 0),
        description="MTOT DEP BANKCARD",
        amount=200.0,
        uuid="0f7a185e-c2d8-44c7-9d9a-9db2c434c595",
    )
    parser = FirstUnitedBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_first_financial_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/first_financial/first_financial_bank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 3, 0, 0),
        description="MTOT DEP BANKCARD CCD",
        amount=9.0,
        uuid="5bfbb910-1c51-4ab8-9015-b6637d09c52b",
    )
    parser = FirstFinancialBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_chase_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/chase/chase.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 3, 0, 0),
        description="Fedwire Credit Via: Vista Bank/111314575 B/O: Prairie House Living Center Plainview TX",
        amount=22686.89,
        uuid="9f70b74d-4e4e-4f67-b558-cb0f219d1a82",
    )
    parser = ChaseBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_cadence_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/cadence/cadence_bank_after_ocr.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 3, 0, 0),
        description="AARP SUPPLEMENTA 1362739571",
        amount=184.05,
        uuid="91703299-d763-4381-866b-bc456eb85354",
    )
    parser = CadenceBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_bank_of_texas():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/bank_of_texas/bank_of_texas.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 4, 0, 0),
        description="36TREAS 310MISC PAY  *****1378360012",
        amount=28276.82,
        uuid="8ed0c310-74b6-42b6-b6d6-2fed37aa6b5e",
    )
    parser = BankOfTexasParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_bank_of_america_merrill_lynch():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/bank_of_america_merrill_lynch/bank_of_america_merrill_lynch.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 3, 0, 0),
        description="Greenville SNF L DES:Settlement ID:000021025511178550",
        amount=1272.86,
        uuid="9c81c62b-4f0f-41c8-9194-298b078e4e4b",
    )
    parser = BankOfAmericaMerrillLynchParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_bankwell_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/bankwell/bankwell_after_ocr.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 3, 0, 0),
        description="NDC SWEEP FAC 774",
        amount=703.6,
        uuid="250044e3-158a-4a45-9d18-ae7b82c8cad9",
    )
    parser = BankWellBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_truist_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/truist/truist_bank_1.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 3, 0, 0),
        description="HCCLAIMPMT HMP HAINES CITY REHABILITA TRN*1*133638778240530*1611103898\\",
        amount=537.76,
        uuid="abe3a010-db97-4243-976d-36ae6b52df75",
    )
    parser = TruistBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_sunflower_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/sunflower/sunflower_bank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 6, 3, 0, 0),
        description="INCOMING WIRE 76165890 PPG FUN D II LLC 062006505",
        amount=8000.0,
        uuid="7f3630c7-3a81-4065-9020-37700efb0417",
    )
    parser = SunflowerBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_customers_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/customers/customers_bank.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 5, 1, 0, 0),
        description="AUTOMATIC TRANSFER",
        amount=90.0,
        uuid="2e28281e-29c1-4ba5-a737-d665a4dab7db",
    )
    parser = CustomersBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_tomball_baylor_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/tomball_baylor/tomball_baylor.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 7, 1, 0, 0),
        description="HCCLAIMPMT UnitedHealthcare",
        amount=640.0,
        uuid="2e28281e-29c1-4ba5-a737-d665a4dab7db",
    )
    parser = TomballBaylorBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()


def test_parse_capital_one_bank():
    logger = logging.getLogger(__name__)
    file_path = "tests/data/banks/capital_one/capital_one.PDF"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 7, 17, 0, 0),
        description="ACH deposit Marketplace",
        amount=2112.76,
        uuid="2e28281e-29c1-4ba5-a737-d665a4dab7db",
    )
    parser = CapitalOneBankParser()
    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]
    _check_the_test(first_transaction, parsed_transaction)
    file.close()
