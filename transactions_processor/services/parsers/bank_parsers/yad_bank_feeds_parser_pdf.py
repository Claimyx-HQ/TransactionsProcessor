import logging
import math
from typing import Any, BinaryIO, Dict, List, Union
from loguru import logger
import tabula
import pandas as pd
import numpy as np
from datetime import datetime
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.csv_parser import CSVParser
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class YadBankFeedsParserPDF(PDFParser):
    def __init__(self) -> None:
        super().__init__([100,200, 600, 670, 1120,1330])
    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        date_str = str(row[0]).replace(" ", "")
        print(row)
        if valid_date(date_str, "%m-%d"):
            amount_str = str(row[3])
            subtraction_amount = str(row[4])
            description_str = row[2]
            if amount_str != "nan" and subtraction_amount == "nan":
                amount = parse_amount(amount_str)
                if valid_amount(amount):
                    return Transaction.from_raw_data(date_str, description_str, amount)
        return None