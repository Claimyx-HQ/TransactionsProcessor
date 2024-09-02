import logging
import math
from typing import Any, BinaryIO, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
from datetime import datetime
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.transactions_parser import TransactionsParser


class BankFeedsParser(TransactionsParser):
    def __init__(self) -> None:
        self.decoded_data = []
        self.formated_data = []
        self.logger = logging.getLogger(__name__)

    def parse_transactions(self, file: BinaryIO, file_name: str | None, file_key: str | None) -> List[Transaction]:
        excel_df = pd.read_csv(file)
        try:
            file.seek(0)
        except:
            pass
        extracted_columns = excel_df.iloc[:, [0, 1, 4, 5]]  # Extracting Date, Text, Amount, BankName
    
        # Step 4: Convert the Date, Text, and BankName columns to strings
        extracted_columns.iloc[:, 0] = extracted_columns.iloc[:, 0].astype(str)  # Date as string
        extracted_columns.iloc[:, 1] = extracted_columns.iloc[:, 1].astype(str)  # Text as string
        extracted_columns.iloc[:, 3] = extracted_columns.iloc[:, 3].astype(str)  # BankName as string (index 3 in extracted_columns)
        
        # Step 5: Convert the Amount column to numeric, coercing errors to NaN
        extracted_columns.iloc[:, 2] = pd.to_numeric(extracted_columns.iloc[:, 2], errors='coerce')
        
        cleaned_columns = extracted_columns.dropna()
        result_array = cleaned_columns.to_numpy().tolist()
        self.decoded_data = [
                Transaction.from_raw_data([str(datetime.strptime(row[0], '%Y-%m-%d')), row[1], row[2], row[3]])
                for row in result_array
            ]

        return self.decoded_data
