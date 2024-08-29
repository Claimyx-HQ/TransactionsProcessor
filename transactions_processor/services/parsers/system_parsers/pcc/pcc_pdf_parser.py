import logging
import math
from typing import BinaryIO, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
import re
from transactions_processor.models.transaction import Transaction
from datetime import datetime

from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)
from transactions_processor.utils.math_utils import parse_amount


class PCCPDFParser(TransactionsParser):
    def __init__(self) -> None:
        self.decoded_data = []
        self.formated_data = []
        self.logger = logging.getLogger(__name__)

    def parse_transactions(
        self, file: BinaryIO, file_extension: str | None, file_key: str | None = None
    ) -> List[Transaction]:
        columns = [70, 150, 250, 400, 500, 600, 670, 850]
        # columns = [34, 120, 210, 300, 400, 490, 580, 670]
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
                valid_row = len(row) == 8 and self._valid_date(row[0])
                if valid_row:
                    amount_string = row[6]
                    date = row[0]
                    description = row[4]
                    amount = parse_amount(amount_string)
                    if math.isnan(amount):  # Skip if amount is NaN
                        continue
                    bank_transactions.append(
                        Transaction.from_raw_data([date, description, amount])
                    )
                    bank_transactions_amounts.append(amount)
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
