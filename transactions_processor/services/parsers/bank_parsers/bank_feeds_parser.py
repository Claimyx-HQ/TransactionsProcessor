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
        date_format = detect_date_format(result_array[0][1])  # First, detect the format
        self.decoded_data = [
                Transaction.from_raw_data([str(parse_date_with_format(row[0], date_format)), row[1], row[2], row[3]])
                for row in result_array
            ]

        return self.decoded_data

def parse_date_with_format(date_str: str, date_format: str) -> datetime:
    # Parse the date string using the provided format
    parsed_date = datetime.strptime(date_str, date_format)
    # Return the datetime object in the standardized format '%Y-%m-%d'
    standardized_date = parsed_date.strftime('%Y-%m-%d')
    return datetime.strptime(standardized_date, '%Y-%m-%d')

def detect_date_format(date_str: str) -> str:
    # Define possible date formats
    date_formats = [
        '%Y-%m-%d',    # e.g., 2023-09-15
        '%m/%d/%Y',    # e.g., 09/15/2023
        '%d/%m/%Y',    # e.g., 15/09/2023
        '%d-%m-%Y',    # e.g., 15-09-2023
        '%m-%d-%Y',    # e.g., 09-15-2023
        '%Y/%m/%d',    # e.g., 2023/09/15
        '%d.%m.%Y',    # e.g., 15.09.2023
        '%m.%d.%Y'     # e.g., 09.15.2023
    ]
    
    # Try parsing the date string with each format
    for date_format in date_formats:
        try:
            # If parsing succeeds, return the format
            datetime.strptime(date_str, date_format)
            return date_format
        except ValueError:
            continue
    
    # If none of the formats match, raise an error
    raise ValueError(f"Date format not recognized for date string: {date_str}")