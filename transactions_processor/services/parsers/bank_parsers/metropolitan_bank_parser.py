from typing import Any, List
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class MetropolitanBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([90, 350, 410, 490])
        self.valid_table = True

    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        if valid_date(row[0]) and self.valid_table:
            date_str, description_str, amount_str = row[0], row[1], row[3]
            if description_str == "Ending Balance":
                self.valid_table = False
                return None
            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data(date_str, description_str, amount)
        return None
