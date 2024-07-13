import logging
import math
from typing import Any, BinaryIO, Callable, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
from transactions_processor.models.transaction import Transaction
from datetime import datetime

from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)
from transactions_processor.utils.date_utils import valid_date, valid_date_split
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class FlagstarBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([80, 504, 576])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        if row[0] == "Deposits":
            self.valid_table = True
        elif row[0] == "Withdraw":
            self.valid_table = False
            return None
        valid_row = valid_date(row[0], "%b %d")
        if valid_row and self.valid_table:
            date_str = row[0]
            formatted_date = datetime.strptime(date_str, "%b %d").strftime("%m/%d")
            amount_str = row[2]
            description_str = row[1]
            amount = parse_amount(amount_str)
            if not valid_amount(amount):
                return None
            transaction = Transaction.from_raw_data(
                [formatted_date, description_str, amount]
            )
            return transaction
        return None
