from abc import abstractmethod
import logging
import math
from typing import Any, BinaryIO, Callable, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
from transactions_processor.models.transaction import Transaction
from datetime import datetime

from transactions_processor.services.parsers.transactions_parser import TransactionsParser


class PDFParser(TransactionsParser):
    def __init__(self, column_positions: List[int]) -> None:
        self.logger = logging.getLogger(__name__)
        self.column_positions = column_positions
        self._enable = True

    # field_indexes is a dictionary that maps the field names to their respective indexes
    # parse_row is a function that takes a row and returns a Transaction object
    def parse_transactions(self, file: BinaryIO) -> List[Transaction]:
        df = tabula.io.read_pdf(
            file,
            multiple_tables=True,
            pages="all",
            pandas_options={"header": None},
            guess=False,
            columns=self.column_positions,
        )
        bank_transactions: List[Transaction] = []

        for table in df:
            table_data: List = table.values.tolist()  # type: ignore
            for i, row  in enumerate(table_data):
                # Signal to stop processing if enable is set to False
                if not self._enable:
                    return bank_transactions
                transaction = self._parse_row(row, i)
                if transaction:
                    bank_transactions.append(transaction)
        return bank_transactions

    @abstractmethod
    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        pass

