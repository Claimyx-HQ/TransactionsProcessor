from datetime import datetime
from transactions_processor.schemas.transaction import Transaction


bank_amounts = [100, 200, 300, 300]
system_amounts = [50, 50, 120, 80, 200, 300]

bank_transactions = [
    Transaction(
        date=datetime(2021, 1, 1),
        description="AAA",
        amount=transaction_amount,
        batch_number=1,
        origin="bank_file.csv",
    )
    for transaction_amount in bank_amounts
]

system_transactions = [
    Transaction(
        date=datetime(2021, 1, 1),
        description="Automatic Transfer",
        amount=transaction_amount,
        batch_number=1,
        origin="system_file.xls",
    )
    for transaction_amount in system_amounts
]
