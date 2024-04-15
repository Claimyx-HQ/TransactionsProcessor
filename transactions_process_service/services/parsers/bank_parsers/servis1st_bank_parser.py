import logging
import math
from typing import BinaryIO, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
from starlette.datastructures import UploadFile
from ..file_parser import FileParser
from transactions_process_service.schemas.transaction import Transaction
from datetime import datetime


class Servis1stBankParser(FileParser):
    def __init__(self) -> None:
        self.decoded_data = []
        self.formated_data = []
        self.logger = logging.getLogger(__name__)

    def parse_transactions(self, file: BinaryIO) -> List[Transaction]:
        columns = [65, 130, 326, 594]
        df = tabula.io.read_pdf(
            file,
            multiple_tables=True,
            pages="all",
            pandas_options={"header": None},
            guess=False,
            columns=columns,
        )
        try:
            file.seek(0)
        except:
            pass
        bank_transactions: List[Transaction] = (
            []
        )  # Use a Python list for accumulating transactions
        bank_transactions_amounts = []  # Likewise, for amounts

        for table in df:
            table_data: List = table.values.tolist()  # type: ignore
            in_deposits = False
            for row in table_data:
                self.logger.debug(f"row length: {len(row)} -- {row}")
                if isinstance(row[1], str):
                    if row[1] == "DEPOSITS":
                        in_deposits = True
                        self.logger.debug(f"For row {row}, in_deposits = {in_deposits}")
                    elif row[1].startswith("WITHDRAW"):
                        in_deposits = False
                        self.logger.debug(f"For row {row}, in_deposits = {in_deposits}")

                valid_row, formatted_date = self._valid_date(row[1])
                if valid_row and in_deposits:
                    amount = (
                        float(row[3].replace(",", "").replace("$", "").replace(" ", ""))
                        if isinstance(row[3], str)
                        else float(row[3])
                    )
                    if math.isnan(amount) or amount <= 0.0:  # Skip if amount is NaN
                        continue
                    description = row[2]
                    date = formatted_date
                    bank_transactions.append(
                        Transaction.from_raw_data([date, description, amount])
                    )
                    bank_transactions_amounts.append(amount)
                    # self.logger.debug(f"row {row}")
        return bank_transactions

    def _valid_date(self, date: str | float) -> bool:
        try:
            if isinstance(date, float):
                return False, date
            parsed_date = datetime.strptime(date, "%m/%d")
            formatted_date = parsed_date.strftime("%m/%d")
            return True, formatted_date
        except ValueError:
            return False, date


# Local Test
