from abc import abstractmethod
import logging
from typing import BinaryIO, List
from transactions_processor.schemas.transaction import Transaction

from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)
import io
import pandas as pd
from loguru import logger


filtered_transaction_descriptions = [
    "Automatic Transfer",
    "Automatic Bank Transfer",
]


class CSVParser(TransactionsParser):
    def __init__(
        self,
        date_col_index,
        description_col_indx: int,
        amount_col_index: int,
        batch_col_index: int | str | None = None,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.date_col_index = date_col_index
        self.description_col_indx = description_col_indx
        self.amount_col_index = amount_col_index
        self.batch_col_index = batch_col_index
        self.file_name = ""

    def parse_transactions(
        self,
        file: BinaryIO,
        file_name: str | None = None,
        file_key: str | None = None,
    ) -> List[Transaction]:
        self.file_name = file_name

        excel_df = self._parse_excel(file)
        column_indexes = [
            self.date_col_index,
            self.description_col_indx,
            self.amount_col_index,
            self.batch_col_index,
        ]
        column_indexes = [index for index in column_indexes if index is not None]

        important_columns = excel_df.iloc[:, column_indexes]

        important_columns = important_columns.dropna()  # Remove missing values (NaN)
        transactions: List[Transaction] = []
        for column in important_columns.to_numpy().tolist():
            transaction = Transaction.from_raw_data(*column, origin=file_name)
            transactions.append(transaction)
        return transactions

    def _parse_excel(self, file: BinaryIO) -> pd.DataFrame:
        excel_df = None
        try:
            logger.info("Trying to parse file as Excel")
            excel_df = pd.read_excel(file, sheet_name=0)
        except Exception as e:
            logger.info(f"Failed to parse file as Excel: {e}\nTrying as CSV")
            file.seek(0)
            try:
                excel_df = pd.read_csv(file)
            except Exception as csv_e:
                logger.error(f"Failed to parse file as CSV: {csv_e}")
                raise ValueError(f"Failed to parse file as Excel or CSV: {e}, {csv_e}")
        try:
            file.seek(0)
        except Exception as e:
            pass
        return excel_df
