from datetime import datetime
from transactions_processor.schemas.transaction import Transaction


bank_transactions = [
    Transaction(
        date=datetime(2021, 1, 1),
        description="AAA",
        amount=100,
        batch_number=1,
        origin="bank_file.csv",
    ),
    Transaction(
        date=datetime(2021, 1, 1),
        description="AAAA",
        amount=200,
        batch_number=2,
        origin="bank_file.csv",
    ),
    Transaction(
        date=datetime(2021, 1, 1),
        description="BBB",
        amount=200,
        batch_number=3,
        origin="bank_file.csv",
    ),
    Transaction(
        date=datetime(2021, 1, 1),
        description="BBB",
        amount=300,
        batch_number=4,
        origin="bank_file.csv",
    ),
    Transaction(
        date=datetime(2021, 1, 1),
        description="CCC",
        amount=500,
        batch_number=5,
        origin="bank_file.csv",
    ),
]

system_transactions = [
    Transaction(
        date=datetime(2021, 1, 1),
        description="Automatic Transfer",
        amount=100,
        batch_number=1,
        origin="system_file.xls",
    ),
    Transaction(
        date=datetime(2021, 1, 1),
        description="Automatic Bank Transfer",
        amount=200,
        batch_number=2,
        origin="system_file.xls",
    ),
    Transaction(
        date=datetime(2021, 1, 1),
        description="Automatic Transfer",
        amount=300,
        batch_number=3,
        origin="system_file.xls",
    ),
    Transaction(
        date=datetime(2021, 1, 1),
        description="Automatic Transfer",
        amount=300,
        batch_number=4,
        origin="system_file.xls",
    ),
    Transaction(
        date=datetime(2021, 1, 1),
        description="Automatic Bank Transfer",
        amount=400,
        batch_number=5,
        origin="system_file.xls",
    ),
]
