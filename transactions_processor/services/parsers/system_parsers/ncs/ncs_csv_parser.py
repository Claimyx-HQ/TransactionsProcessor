from typing import BinaryIO, List
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.csv_parser import CSVParser
from transactions_processor.utils.excel_utils import (
    get_csv_first_cell,
    get_xls_first_cell,
    get_xlsx_first_cell,
)


class NCSCSVParser(CSVParser):
    def __init__(self) -> None:
        super().__init__(0, 3, 1, 6)

    def parse_transactions(
        self,
        file: BinaryIO,
        file_name: str | None = "",
        file_key: str | None = None,
    ) -> List[Transaction]:
        first_cell = self._get_first_excel_cell(file, file_name or "")
        if first_cell == "Date":
            self.date_col_index = 0
            self.description_col_indx = 1
            self.amount_col_index = 3
            self.batch_col_index = 7
        return super().parse_transactions(file, file_name, file_key)

    def _get_first_excel_cell(self, file: BinaryIO, file_name: str) -> str:
        file_extension = file_name.split(".")[-1]
        if file_extension == "xlsx":
            return get_xlsx_first_cell(file)
        elif file_extension == "xls":
            return get_xls_first_cell(file)
        elif file_extension == "csv":
            return get_csv_first_cell(file)
        raise ValueError("Invalid file extension")

        # return super().parse_transactions(file, file_name, file_key)
