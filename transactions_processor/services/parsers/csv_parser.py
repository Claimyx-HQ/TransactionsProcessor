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
        gl_account_col_index: int | str | None = None,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.date_col_index = date_col_index
        self.description_col_indx = description_col_indx
        self.amount_col_index = amount_col_index
        self.batch_col_index = batch_col_index
        self.gl_account_col_index = gl_account_col_index

    def parse_transactions(
        self,
        file: BinaryIO,
        file_name: str | None = "",
        file_key: str | None = None,
    ) -> List[Transaction]:
        logger.info("Parsing transactions file")
        self.file_name = file_name
        excel_df = self._parse_excel(file)
        logger.info("Extracting Transactions")
        column_mapping = {
            "date": self.date_col_index,
            "description": self.description_col_indx,
            "amount": self.amount_col_index,
            "batch_number": self.batch_col_index,
            "gl_account_number": self.gl_account_col_index,
        }
        column_mapping = {
            key: index for key, index in column_mapping.items() if index is not None
        }
        column_indexes = list(column_mapping.values())

        important_columns = excel_df.iloc[:, column_indexes]
        important_columns.columns = list(column_mapping.keys())
        important_columns = important_columns.dropna()  # Remove missing values (NaN)

        transactions = self._parse_transactions(important_columns, str(file_name))

        logger.info(f"Extracted {len(transactions)} transactions")
        return transactions

    def _parse_excel(self, file: BinaryIO) -> pd.DataFrame:
        try:
            logger.info("Trying to parse file as Excel")
            excel_df = pd.read_excel(file, sheet_name=0)
            file.seek(0)
            return excel_df
        except Exception as e:
            logger.info(f"Failed to parse file as Excel: {e}\nTrying as CSV")
            file.seek(0)
            try:
                excel_df = pd.read_csv(file)
                logger.info(f"Successfully parsed CSV data")
                return excel_df

            except Exception as csv_e:
                logger.error(f"Failed to parse file as CSV: {csv_e}")
                raise ValueError(f"Failed to parse file as Excel or CSV: {e}, {csv_e}")

    def _parse_transactions(
        self, columns: pd.DataFrame, file_name: str
    ) -> List[Transaction]:
        transactions: List[Transaction] = []
        for _, row in columns.iterrows():
            try:
                transaction_data = row.to_dict()

                # Prepare arguments for Transaction.from_raw_data
                raw_data = {
                    "date": transaction_data.get("date"),
                    "description": transaction_data.get("description"),
                    "amount": transaction_data.get("amount"),
                    "batch_number": transaction_data.get("batch_number"),
                    "origin": transaction_data.get("gl_account_number", file_name),
                }

                # Remove None values from raw_data
                raw_data = {k: v for k, v in raw_data.items() if v is not None}

                # Create Transaction object using keyword arguments
                transaction = Transaction.from_raw_data(**raw_data)
                transactions.append(transaction)

            except Exception as e:
                logger.error(f"Failed to parse transaction: {e}")
        return transactions
