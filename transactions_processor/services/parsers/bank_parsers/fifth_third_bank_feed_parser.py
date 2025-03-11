from typing import Any, BinaryIO, Dict, List, Union
from loguru import logger
import tabula
import pandas as pd
import numpy as np
from datetime import datetime
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.csv_parser import CSVParser
from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)


class FifthThirdBankFeedParser(CSVParser):
    def __init__(self) -> None:
        super().__init__(date_col_index=0, description_col_indx=2, amount_col_index=5)
