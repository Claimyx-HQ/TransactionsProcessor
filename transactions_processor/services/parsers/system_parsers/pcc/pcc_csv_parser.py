import logging
import math
from typing import BinaryIO, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
import re
from transactions_processor.schemas.transaction import Transaction
from datetime import datetime

from transactions_processor.services.parsers.csv_parser import CSVParser
from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)
from transactions_processor.utils.math_utils import parse_amount


class PCCCSVParser(CSVParser):
    def __init__(self) -> None:
        super().__init__(0, 6, 7, 4, 9)
