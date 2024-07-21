import logging
import math
from typing import BinaryIO, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
import re
from transactions_processor.models.transaction import Transaction
from datetime import datetime

from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)
from transactions_processor.utils.math_utils import parse_amount


class PCCCSVParser(TransactionsParser):
    def __init__(self) -> None:
        self.decoded_data = []
        self.formated_data = []
        self.logger = logging.getLogger(__name__)

    def parse_transactions(
        self, file: BinaryIO, file_key: str | None = None
    ) -> List[Transaction]:
        excel_df = None
        print("trying as excel")
        try:
            excel_df = pd.read_excel(file, sheet_name=0)
        except Exception as e:
            print("trying as csv")
            file.seek(0)
            try:
                excel_df = pd.read_csv(file)
            except Exception as csv_e:
                raise ValueError(f"Failed to parse file as Excel or CSV: {e}, {csv_e}")
        # excel_df = pd.read_excel(
        #     file, sheet_name=0
        # )  # Assuming that always the first sheet is the table, if not then use pd.read_excel(self.file_path, sheet_name=<"Sheet Name">)
        try:
            file.seek(0)
        except:
            pass
        important_columns = excel_df.iloc[:, [0, 7, 6]]
        if pd.api.types.is_numeric_dtype(important_columns):
            # If the column is already numeric, directly convert to array
            system_transactions = important_columns.to_numpy()
        else:
            # If it contains non-numeric values, filter and convert
            important_columns = (
                important_columns.dropna()
            )  # Remove missing values (NaN)
            self.decoded_data = [
                transaction
                for transaction in [
                    Transaction.from_raw_data(trans)
                    for trans in important_columns.to_numpy().tolist()
                ]
            ]

            numeric_values = important_columns.iloc[:, 1].to_list()
            system_transactions = np.array(
                [float(val) for val in numeric_values if float(val) > 0.0]
            )
        # self.logger.info(df)
        return self.decoded_data
