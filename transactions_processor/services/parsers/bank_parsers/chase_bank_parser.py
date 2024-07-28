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


class ChaseBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([81,455,535])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        title = str(str(row[0]) + str(row[1]) ).lower()
        for title_type in ['DEBITS','DAILY', 'BALANCE', 'SUMMARY']:
            if title_type.lower() in title:
                self.valid_table = False
        for title_type in ['CREDIT','DEPOSIT','ADDITIONS']:
            if title_type.lower() in title:
                self.valid_table = True
        
        date_str = row[0] 
        valid_row = valid_date(date_str, "%m/%d")
        amount_str = row[2] 
        description_str = row[1] 
        if valid_row and self.valid_table and amount_str:
            amount = parse_amount(amount_str) 
            if not valid_amount(amount):
                return None
            transaction = Transaction.from_raw_data([date_str, description_str, amount])
            return transaction
   
        return None
