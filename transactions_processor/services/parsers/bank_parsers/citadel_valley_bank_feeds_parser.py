from typing import BinaryIO, List

from loguru import logger
import pandas as pd
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.csv_parser import CSVParser

class CitadelValleyBankFeedsParser(CSVParser):
    def __init__(self) -> None:
        super().__init__(1, 3, 5, batch_col_index=None, gl_account_col_index=0)
    