from typing import Any, List
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class HuntingtonBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([100, 170])
        self.valid_table = True

    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        if isinstance(row[1], str) and "(-)" in row[1]:
            self._enable = False
            return None
        if valid_date(row[0], "%m/%d") and self.valid_table:
            date_str, amount_str, description_str = row[0], row[1], row[2]
            amount = parse_amount(amount_str)
            if not valid_amount(amount):
                return None
            return Transaction.from_raw_data([date_str, description_str, amount])
        return None
