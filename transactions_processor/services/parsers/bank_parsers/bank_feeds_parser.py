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

    def parse_transactions(self, file: BinaryIO) -> List[Transaction]:
        excel_df = pd.read_csv(file)
        try:
            file.seek(0)
        except:
            pass
        extracted_columns = excel_df.iloc[:, [0, 1, 4]]
        extracted_columns.iloc[:, 0] = extracted_columns.iloc[:, 0].astype(str)
        extracted_columns.iloc[:, 1] = extracted_columns.iloc[:, 1].astype(str)

        extracted_columns.iloc[:, 2] = pd.to_numeric(extracted_columns.iloc[:, 2], errors='coerce')

        cleaned_columns = extracted_columns.dropna()
        result_array = cleaned_columns.to_numpy().tolist()
        self.decoded_data = [
                Transaction(date=datetime.strptime(row[0], '%Y-%m-%d'), description=row[1], amount=row[2])
                for row in result_array
            ]

        return self.decoded_data
