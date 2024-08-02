from abc import abstractmethod
import logging
from typing import Any, BinaryIO, Callable, Dict, List, Union
import tabula
from transactions_processor.models.transaction import Transaction
from datetime import datetime

from transactions_processor.services.converters.scanned_pdf_converter import (
    ScannedPDFConverter,
)
from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)


class PDFParser(TransactionsParser):
    def __init__(self, column_positions: List[float]) -> None:
        self.logger = logging.getLogger(__name__)
        self.column_positions = column_positions
        self.pdf_converter = ScannedPDFConverter()
        self._enable = True

    # field_indexes is a dictionary that maps the field names to their respective indexes
    # parse_row is a function that takes a row and returns a Transaction object
    def parse_transactions(
        self, file: BinaryIO, file_key: str | None = None
    ) -> List[Transaction]:
        tables = self._parse_pdf(file)
        if len(tables) == 0:
            if not file_key:
                return []
            print("No tables found in PDF, converting to text and trying again.")
            file.seek(0)
            converted_pdf = self.pdf_converter.get_converted_pdf(file_key)
            if not converted_pdf:
                return []
            tables = self._parse_pdf(converted_pdf)

        bank_transactions: List[Transaction] = []

        for table in tables:
            table_data: List = table.values.tolist()  # type: ignore
            for i, row in enumerate(table_data):
                # Signal to stop processing if enable is set to False
                if not self._enable:
                    return bank_transactions
                try:
                    transaction = self._parse_row(row, i)
                except:
                    transaction = None
                if transaction:
                    bank_transactions.append(transaction)
        return bank_transactions

    def _parse_pdf(self, file: BinaryIO) -> List[Transaction]:
        tables = tabula.io.read_pdf(
            file,
            multiple_tables=True,
            pages="all",
            pandas_options={"header": None},
            guess=False,
            columns=self.column_positions,
        )
        return tables # type: ignore

    @abstractmethod
    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        pass
