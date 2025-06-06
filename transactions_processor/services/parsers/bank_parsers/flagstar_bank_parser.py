import logging
import math
from typing import BinaryIO, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
from transactions_processor.models.transaction import Transaction
from datetime import datetime

from transactions_processor.services.parsers.transactions_parser import TransactionsParser


class FlagstarBankParser(TransactionsParser):
    def __init__(self) -> None:
        self.decoded_data = []
        self.formated_data = []
        self.logger = logging.getLogger(__name__)

    def parse_transactions(self, file: BinaryIO) -> List[Transaction]:
        columns = [80, 504, 576]
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
                self.logger.debug(f"row length: {len(row)} -- {row}")
                if row[0] == "Deposits":
                    in_deposits = True
                elif row[0] == "Withdraw":
                    in_deposits = False
                valid_row, formatted_date = self._valid_date(row[0])
                if valid_row and in_deposits:

                    amount = (
                        float(row[2].replace(",", "").replace("$", "").replace(" ", ""))
                        if isinstance(row[2], str)
                        else float(row[2])
                    )
                    if math.isnan(amount) or amount <= 0.0:  # Skip if amount is NaN
                        continue
                    description = row[1]
                    date = formatted_date
                    bank_transactions.append(
                        Transaction.from_raw_data([date, description, amount])
                    )
                    bank_transactions_amounts.append(amount)
                    # self.logger.debug(f"row {row}")
        return bank_transactions

    def _valid_date(self, date: str | float) -> bool:
        try:
            if isinstance(date, float):
                return False, date
            parsed_date = datetime.strptime(date, "%b %d")
            formatted_date = parsed_date.strftime("%m/%d")
            return True, formatted_date
        except ValueError:
            return False, date


# Local Test
