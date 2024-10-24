from typing import Any, List, Optional
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class BHIBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([80, 350, 430, 480])
        self.valid_table = True

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        date_str = str(row[0])
        if not valid_date(date_str, "%m/%d") or not self.valid_table:
            return None

        description_str = str(row[1])
        amount_str = str(row[3])

        if description_str == "ENDING BALANCE":
            self.valid_table = False
            return None

        try:
            amount = parse_amount(amount_str)
        except ValueError:
            return None

        if not valid_amount(amount):
            return None

        return Transaction.from_raw_data(date_str, description_str, amount)
