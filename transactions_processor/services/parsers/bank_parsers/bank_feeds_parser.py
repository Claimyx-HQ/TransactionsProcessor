import logging
import math
from typing import Any, BinaryIO, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
from datetime import datetime
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.csv_parser import CSVParser
from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)


class BankFeedsParser(CSVParser):
    def __init__(self) -> None:
        super().__init__(0, 1, 4)
