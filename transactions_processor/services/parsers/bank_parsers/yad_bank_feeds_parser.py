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
from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)


class YadBankFeedsParser(CSVParser):
    def __init__(self) -> None:
        super().__init__(date_col_index=2,description_col_indx=6,amount_col_index=3, gl_account_col_index=0)
        self.additional_description_col_index = 8
    def parse_transactions(
        self,
        file: BinaryIO,
        file_name: str | None = None,
        file_key: str | None = None,
    ) -> List[Transaction]:
        try:
            self.file_name = file_name
            excel_df = self._parse_excel(file)
        except Exception as e:
            logger.error(f"Failed to parse file: {e}")
            raise e
        try:
            column_mapping = {
                'date': self.date_col_index,
                'description': self.description_col_indx,
                'additional_description': self.additional_description_col_index,
                'amount': self.amount_col_index,
                'batch_number': self.batch_col_index,
                'gl_account_number': self.gl_account_col_index,
            }
            # Remove any None values from column_mapping
            column_mapping = {key: index for key, index in column_mapping.items() if index is not None}
            column_indexes = list(column_mapping.values())

            important_columns = excel_df.iloc[:, column_indexes]
            important_columns.columns = list(column_mapping.keys())
            # Drop rows only if 'date', 'description', or 'amount' are missing
            important_columns = important_columns.dropna(subset=['date', 'description', 'amount'])

            transactions: List[Transaction] = []
            for _, row in important_columns.iterrows():
                try:
                    transaction_data = row.to_dict()

                    # Combine descriptions
                    description = str(transaction_data.get('description', '')).strip()
                    additional_description = str(transaction_data.get('additional_description', '')).strip()
                    if additional_description:
                        full_description = f"{description} - {additional_description}"
                    else:
                        full_description = description

                    # Prepare arguments for Transaction.from_raw_data
                    raw_data = {
                        'date': transaction_data.get('date'),
                        'description': full_description,
                        'amount': transaction_data.get('amount'),
                        'batch_number': transaction_data.get('batch_number'),
                        'origin': str(int(transaction_data.get('gl_account_number')) or file_name),
                    }

                    # Remove None values from raw_data
                    raw_data = {k: v for k, v in raw_data.items() if v is not None}

                    # Create Transaction object using keyword arguments
                    transaction = Transaction.from_raw_data(**raw_data)
                    transactions.append(transaction)
                except Exception as e:
                    logger.error(f"Failed to parse transaction: {e}")
            return transactions
        except Exception as e:
            logger.error(f"Failed to parse transactions: {e}")  
            raise e