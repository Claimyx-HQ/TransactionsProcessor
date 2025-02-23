from datetime import datetime

from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.system_parsers.ncs.ncs_csv_parser import (
    NCSCSVParser,
)
from transactions_processor.services.parsers.system_parsers.ncs.ncs_parser import (
    NCSParser,
)
from transactions_processor.services.parsers.system_parsers.ncs.ncs_pdf_parser import (
    NCSPDFParser,
)
from transactions_processor.services.parsers.system_parsers.pcc.pcc_parser import (
    PCCParser,
)


def test_parse_ncs_file():
    file_path = "tests/data/system/NCS/version_1/ncs.xls"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2023, 10, 1, 0, 0),
        description="gnss wire",
        amount=-37438.65,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
        batch_number=1302,
        origin="ncs.xls",
    )
    parser = NCSParser()

    transactions = parser.parse_transactions(file, "ncs.xls")
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
    assert first_transaction.batch_number == parsed_transaction.batch_number
    assert first_transaction.origin == parsed_transaction.origin

    file.close()


def test_parse_ncs_file_bad_foregin_encoding():
    file_path = "tests/data/system/NCS/version_1/ncs-foreign-encoding.csv"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 9, 1, 0, 0),
        description="Anthem (part of 66,187.59)",
        amount=8023.03,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
        batch_number=5237,
        origin="ncs-foreign-encoding.csv",
    )
    parser = NCSParser()

    transactions = parser.parse_transactions(file, "ncs-foreign-encoding.csv")
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
    assert first_transaction.batch_number == parsed_transaction.batch_number
    assert first_transaction.origin == parsed_transaction.origin

    file.close()


def test_parse_ncs_file2():
    file_path = "tests/data/system/NCS/version_2/ncs.xlsx"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 12, 1, 0, 0),
        description="Really should be PNC. trans to PC acct",
        amount=0.0,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
        batch_number=18923,
        origin="ncs.xlsx",
    )
    parser = NCSParser()

    transactions = parser.parse_transactions(file, "ncs.xlsx")
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
    assert first_transaction.batch_number == parsed_transaction.batch_number
    assert first_transaction.origin == parsed_transaction.origin

    file.close()


def test_parse_ncs_file2_2():
    file_path = "tests/data/system/NCS/version_2/ncs2.xlsx"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2025, 1, 2, 0, 0),
        description="RFMS",
        amount=1067.44,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
        batch_number=18819,
        origin="ncs2.xlsx",
    )
    parser = NCSParser()

    transactions = parser.parse_transactions(file, "ncs2.xlsx")
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
    assert first_transaction.batch_number == parsed_transaction.batch_number
    assert first_transaction.origin == parsed_transaction.origin

    file.close()


def test_parse_ncs_pdf_file():
    file_path = "tests/data/system/NCS/version_1/ncs.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 9, 1, 0, 0),
        description="BCBS In Process 07/01",
        amount=599.76,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
        batch_number="6726",
        origin="ncs.pdf",
    )
    parser = NCSParser()

    transactions = parser.parse_transactions(file, "ncs.pdf")
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
    assert first_transaction.batch_number == parsed_transaction.batch_number
    assert first_transaction.origin == parsed_transaction.origin

    file.close()


def test_parse_ncs_pdf_file2():
    file_path = "tests/data/system/NCS/version_2/ncs.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 1, 1, 0, 0),
        description="CC",
        amount=1000.0,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
        batch_number="25641",
        origin="ncs.pdf",
    )
    parser = NCSParser()

    transactions = parser.parse_transactions(file, "ncs.pdf")
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
    assert first_transaction.batch_number == parsed_transaction.batch_number
    assert first_transaction.origin == parsed_transaction.origin

    file.close()


def test_parse_pcc_pdf():
    file_path = "tests/data/system/PCC/PCC.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 4, 1, 0, 0),
        description="Credit Card 04/01/2024",
        amount=400.0,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
        batch_number=2862,
        origin="1010-409-00",
    )
    parser = PCCParser()

    transactions = parser.parse_transactions(file, "pcc.pdf")
    parsed_transaction = transactions[1]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
    assert first_transaction.batch_number == parsed_transaction.batch_number
    assert first_transaction.origin == parsed_transaction.origin

    file.close()


def test_parse_pcc_pdf2():
    file_path = "tests/data/system/PCC/PCC2.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 10, 1, 0, 0),
        description="Insurance Co-Insurance A 10/01/2024",
        amount=5916.0,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
        batch_number=3929,
        origin="1010-409-00",
    )
    parser = PCCParser()

    transactions = parser.parse_transactions(file, "pcc.pdf")
    parsed_transaction = transactions[1]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
    assert first_transaction.batch_number == parsed_transaction.batch_number
    assert first_transaction.origin == parsed_transaction.origin

    file.close()


def test_parse_pcc_excel():
    file_path = "tests/data/system/PCC/PCC.xlsx"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 5, 2, 0, 0),
        description="Anthem 05/02/2024",
        amount=70.20,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
        batch_number=4266,
        origin="1010-409-00",
    )
    parser = PCCParser()

    transactions = parser.parse_transactions(file, "pcc.xlsx")
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount
    assert first_transaction.batch_number == parsed_transaction.batch_number
    assert first_transaction.origin == parsed_transaction.origin

    file.close()
