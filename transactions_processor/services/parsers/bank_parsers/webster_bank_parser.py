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
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class WebsterBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([34, 120, 210, 300, 400, 490, 580, 670])
        self.valid_table = True


    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        valid_row = len(row) == 7 and valid_date(row[1])
        if valid_row and self.valid_table:
            date_str = row[1]
            amount_str = row[5]
            description_str = row[2]
            if(description_str == 'Ending Balance'):
                self.valid_table = False
                return None
            amount = parse_amount(amount_str)
            if not valid_amount(amount):
                return None
            transaction = Transaction.from_raw_data([date_str, description_str, amount])
            return transaction
        return None
