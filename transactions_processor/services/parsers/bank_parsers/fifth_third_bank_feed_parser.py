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
from typing import BinaryIO, List
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.csv_parser import CSVParser
from transactions_processor.utils.excel_utils import (
    get_csv_first_cell,
    get_xls_first_cell,
    get_xlsx_first_cell,
)


class FifthThirdBankFeedParser(CSVParser):
    def __init__(self) -> None:
        super().__init__(date_col_index=0, description_col_indx=2, amount_col_index=5)

    def parse_transactions(
        self,
        file: BinaryIO,
        file_name: str | None = "",
        file_key: str | None = None,
    ) -> List[Transaction]:
        # TODO: Check where file name could be None
        if not file_name:
            raise ValueError("file name is required")
        first_cell = self._get_first_excel_cell(file, file_name)
        if first_cell == "Date":
            self.date_col_index = 0
            self.description_col_indx = 2
            self.amount_col_index = 5
        else:
            self.date_col_index = 2
            self.description_col_indx = 4
            self.amount_col_index = 6

        return super().parse_transactions(file, file_name, file_key)

    def _get_first_excel_cell(self, file: BinaryIO, file_name: str) -> str:
        file_extension = file_name.split(".")[-1].lower()
        if file_extension == "xlsx":
            return get_xlsx_first_cell(file)
        elif file_extension == "xls":
            return get_xls_first_cell(file)
        elif file_extension == "csv":
            return get_csv_first_cell(file)
        file.seek(0)
        raise ValueError("Invalid file extension")

        # return super().parse_transactions(file, file_name, file_key)
