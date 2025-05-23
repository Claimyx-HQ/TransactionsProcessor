import logging
import math
from typing import BinaryIO, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
from tabula.util import FileLikeObj
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.transactions_parser import TransactionsParser


class ForbrightBankParser(TransactionsParser):
    def __init__(self) -> None:
        self.decoded_data = []
        self.formated_data = []
        self.logger = logging.getLogger(__name__)

    def parse_transactions(self, file: BinaryIO) -> List[Transaction]:

        columns = [50, 150, 400]
        df = tabula.io.read_pdf(
            file,
            multiple_tables=True,
            pages="all",
            pandas_options={"header": None},
            guess=False,
            columns=columns,
        )
        # df = tabula.io.read_pdf(
        #     file,
        #     multiple_tables=True,
        #     pages="all",
        #     pandas_options={"header": None},
        #     guess=False,
        #
        # )
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
            found_start = False  # Initially, we haven't found the start marker
            for row in table_data:
                if len(row) == 4 and row[3] == "Additions":
                    found_start = True  # Start marker found
                elif (
                    found_start and len(row) == 4
                ):  # Process transactions after finding the start
                    try:
                        amount = (
                            float(row[3].replace(",", ""))
                            if isinstance(row[3], str)
                            else float(row[3])
                        )
                        if math.isnan(amount) or amount <= 0.0:  # Skip if amount is NaN
                            continue
                        bank_transactions_amounts.append(
                            amount
                        )  # Append amount to list
                        raw_data = [row[1], amount, row[2]]
                        # new_row = row[0].split(" ", 1) + [
                        #     amount
                        # ]  # Prepare new transaction row, row[0] has the date and description i  the same index
                        bank_transactions.append(
                            Transaction.from_raw_data(raw_data)
                        )  # Append new transaction row to list
                    except Exception as e:
                        self.logger.exception(e)
                        continue
        return bank_transactions
