from datetime import datetime

from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.system_parsers.ncs_parser import NCSParser
from transactions_processor.services.parsers.system_parsers.pcc_parser import PCCParser


def test_parse_ncs_file():
    file_path = "tests/data/system/NCS/bankst.xls"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2023, 10, 1, 0, 0),
        description="gnss wire",
        amount=-37438.65,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
    )
    parser = NCSParser()

    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount

    file.close()


def test_parse_pcc():
    file_path = "tests/data/system/PCC/PCC.pdf"
    file = open(file_path, "rb")
    first_transaction = Transaction(
        date=datetime(2024, 4, 1, 0, 0),
        description="Credit Card 04/01/202",
        amount=400.0,
        uuid="80164d55-8276-4802-96d0-7b14889d2908",
    )
    parser = PCCParser()

    transactions = parser.parse_transactions(file)
    parsed_transaction = transactions[0]

    assert first_transaction.date == parsed_transaction.date
    assert first_transaction.description == parsed_transaction.description
    assert first_transaction.amount == parsed_transaction.amount

    file.close()
