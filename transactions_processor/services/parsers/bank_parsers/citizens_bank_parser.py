from typing import Any, List, Optional
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class CitizensBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([100, 158, 430])
        self.valid_table = True

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        date_str, amount_str, description_str = map(str, row[:3])
        date_str_lower = date_str.lower()

        if any(
            keyword in date_str_lower for keyword in ["other debits", "daily balance"]
        ):
            self.valid_table = False
            return None
        if "deposits" in date_str_lower:
            self.valid_table = True

        if valid_date(date_str, "%m/%d") and self.valid_table:
            try:
                amount = parse_amount(amount_str)
                if not valid_amount(amount):
                    return None
            except ValueError:
                return None

            return Transaction.from_raw_data(date_str, description_str, amount)

        return None
