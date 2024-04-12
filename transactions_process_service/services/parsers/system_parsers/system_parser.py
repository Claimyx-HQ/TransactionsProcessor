import logging
import math
from typing import Any, Dict, List, Union
from fastapi import UploadFile
import tabula
import pandas as pd
import numpy as np
from transactions_process_service.schemas.transaction import Transaction
from transactions_process_service.services.parsers.file_parser import FileParser


class PharmBillsParser(FileParser):
    def __init__(self) -> None:
        self.decoded_data = []
        self.formated_data = []
        self.logger = logging.getLogger(__name__)

    def parse_transactions(self, file: UploadFile | str) -> List[Transaction]:
        if type(file) is str:
            excel_df = pd.read_excel(
                file, sheet_name=0
            )  # Assuming that always the first sheet is the table, if not then use pd.read_excel(self.file_path, sheet_name=<"Sheet Name">)
        else:
            excel_df = pd.read_excel(
                file.file, sheet_name=0
            )  # Assuming that always the first sheet is the table, if not then use pd.read_excel(self.file_path, sheet_name=<"Sheet Name">)
            file.file.seek(0)
        important_columns = excel_df.iloc[:, [0, 1, 3]]
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
