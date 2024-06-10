import logging
import math
from typing import BinaryIO, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
from transactions_processor.models.transaction import Transaction
from datetime import datetime

from transactions_processor.services.parsers.transactions_parser import TransactionsParser


class UnitedBankParser(TransactionsParser):
    def __init__(self) -> None:
        self.decoded_data = []
        self.formated_data = []
        self.logger = logging.getLogger(__name__)

    def parse_transactions(self, file: BinaryIO) -> List[Transaction]:
        columns = [50, 100, 350, 435, 515]
        df = tabula.io.read_pdf(
            file,
            multiple_tables=True,
            pages="all",
            pandas_options={"header": None},
            guess=False,
            columns=columns,
        )
        try:
            file.seek(0)
        except:
            pass
        bank_transactions: List[Transaction] = (
            []
        )  # Use a Python list for accumulating transactions
        bank_transactions_amounts = []  # Likewise, for amounts

        for table in df:
            table_data: List = table.values.tolist()  # type: ignore
            for row in table_data:
                valid_row = len(row) == 6 and self._valid_date(row[1])
                if valid_row:
                    amount = (
                        float(row[4].replace(",", "").replace("$", "").replace(" ", ""))
                        if isinstance(row[4], str)
                        else float(row[4])
                    )
                    if math.isnan(amount) or amount <= 0.0:  # Skip if amount is NaN
                        continue
                    description = row[2]
                    date = row[1]
                    bank_transactions.append(
                        Transaction.from_raw_data([date, description, amount])
                    )
                    bank_transactions_amounts.append(amount)
                    # self.logger.debug(f"row {row}")
        return bank_transactions

    def _valid_date(self, date: str | float) -> bool:
        try:
            if isinstance(date, float):
                return False
            datetime.strptime(date, "%m/%d/%Y")
            return True
        except ValueError:
            return False


# Local Test
