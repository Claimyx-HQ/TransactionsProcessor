import logging
import math
from typing import Dict, List, Union
import tabula
import pandas as pd
import numpy as np
from ..file_parser import FileParser
from transactions_process_service.schemas.transaction import Transaction
from datetime import datetime


class UnitedBankParser(FileParser):
    def __init__(self) -> None:
        self.decoded_data = []
        self.formated_data = []
        self.logger = logging.getLogger(__name__)

    def parse_transactions(self, file_path: str) -> List[Transaction]:
        df = tabula.io.read_pdf(
            file_path,
            multiple_tables=True,
            pages="all",
            pandas_options={"header": None},
            guess=False,
            columns=[50, 100, 350, 435, 515],
        )
        bank_transactions: List[
            Transaction
        ] = []  # Use a Python list for accumulating transactions
        bank_transactions_amounts = []  # Likewise, for amounts

        for table in df:
            table_data: List = table.values.tolist()  # type: ignore
            for row in table_data:
                valid_row = len(row) == 6 and self._valid_date(row[1])
                if valid_row:
                    amount = (
                        float(row[4].replace(",", "").replace("$", "").replace(" ", ""))
                        if isinstance(row[4], str)
                        else float(row[4])
                    )
                    if math.isnan(amount) or amount <= 0.0:  # Skip if amount is NaN
                        continue
                    bank_transactions_amounts.append(amount)

        print(bank_transactions_amounts)
        return []

    def _valid_date(self, date: str | float) -> bool:
        try:
            if isinstance(date, float):
                return False
            datetime.strptime(date, "%m/%d/%Y")
            return True
        except ValueError:
            return False

# Local Test
        
logging.basicConfig(
    filename="united_bank_parser.log",
    filemode="w",
    format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)
logger.info("App started")
file_path = "tests/data/united_bank.pdf"

parser = UnitedBankParser()
transactions = parser.parse_transactions(file_path)
logger.info(transactions)
