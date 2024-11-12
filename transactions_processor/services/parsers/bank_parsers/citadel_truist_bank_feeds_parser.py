from typing import BinaryIO, List

from loguru import logger
import pandas as pd
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.csv_parser import CSVParser

class CitadelTruistBankFeedsParser(CSVParser):
    def __init__(self) -> None:
        super().__init__(0, 3, 4)
    def parse_transactions(
        self,
        file: BinaryIO,
        file_name: str | None = None,
        file_key: str | None = None,
    ) -> List[Transaction]:
        self.file_name = file_name

        excel_df = self._parse_excel(file)
        
        excel_df = excel_df[excel_df.iloc[:, 1].astype(str).str.lower() == 'credit']

        column_indexes = [
            self.date_col_index,
            self.description_col_indx,
            self.amount_col_index,
            self.batch_col_index,
            self.gl_account_col_index
        ]
        column_indexes = [index for index in column_indexes if index is not None]

        important_columns = excel_df.iloc[:, column_indexes]

        important_columns = important_columns.dropna()  # Remove missing values (NaN)
        transactions: List[Transaction] = []
        for column in important_columns.to_numpy().tolist():
            if self.gl_account_col_index is not None:
                transaction = Transaction.from_raw_data(*column)
            else:
                transaction = Transaction.from_raw_data(*column, origin=file_name)
            transactions.append(transaction)
        return transactions

