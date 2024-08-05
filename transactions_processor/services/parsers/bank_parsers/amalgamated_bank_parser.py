from typing import Any, List, Optional
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class AmalgamatedBankParser(PDFParser):
    INVALID_TITLE_TYPES = {"non-check debits", "daily balance summary", "summary"}
    VALID_TITLE_TYPE = "credits"

    def __init__(self) -> None:
        super().__init__([74, 410, 490, 565])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        date_str = row[0]
        description_str = row[1]
        amount_str = row[2]
        title = f"{date_str}{description_str}".lower()

        # Check for invalid title types
        if any(invalid_type in title for invalid_type in self.INVALID_TITLE_TYPES):
            self.valid_table = False
        elif self.VALID_TITLE_TYPE in title:
            self.valid_table = True

        # Validate the date and amount, then create a Transaction if valid
        if self.valid_table and valid_date(date_str, "%m/%d") and amount_str:
            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data([date_str, description_str, amount])

        return None
