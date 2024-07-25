import logging
import math
from typing import Any, BinaryIO, Callable, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
from transactions_processor.models.transaction import Transaction
from datetime import datetime

from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.services.parsers.transactions_parser import TransactionsParser
from transactions_processor.utils.date_utils import valid_date, valid_date_split
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class CitizensBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([100, 158, 430])
        self.valid_table = True

    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        date_str = row[0]
        valid_row = valid_date(date_str, "%m/%d")
        amount_str = row[1]
        description_str = row[2]
        if date_str == 'Other Debits' or date_str == 'Daily Balance' :
            self.valid_table = False
        if 'Deposits' in str(date_str) :
            self.valid_table = True
        print(row)
        print(valid_row, self.valid_table)
        if valid_row and self.valid_table:
            amount = parse_amount(amount_str)
            if not valid_amount(amount):
                return None
            transaction = Transaction.from_raw_data([date_str, description_str, amount])
            return transaction
        return None
