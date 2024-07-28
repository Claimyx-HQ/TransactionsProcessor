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


class SimmonsBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([70, 260, 430])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        date_str = str(row[0]).replace(' ', '')
        valid_row = valid_date(date_str, "%m/%d")
        amount_str = row[2]
        description_str = row[1]
        title = (str(date_str) + str(description_str) ) 
        for title_type in ['FEE', 'DEBITS','DAILY BALANCE', 'SUMMARY', 'WITHDRAWALS']:
            if title_type.lower() in title.lower():
                self.valid_table = False
        for title_type in ['CREDIT', 'DEPOSIT','ADDITIONS']:
            if title_type.lower() in title.lower():
                self.valid_table = True
        if valid_row and self.valid_table and amount_str:
            amount = parse_amount(amount_str)
            if not valid_amount(amount):
                return None
            transaction = Transaction.from_raw_data([date_str, description_str, amount])
            return transaction
        return None
