from typing import Any, List, Optional
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class ChaseBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([81, 455, 535])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        date_str = str(row[0])
        description_str = str(row[1])
        amount_str = str(row[2])

        title = (date_str + description_str).lower()
        if any(word in title for word in ["debits", "daily", "balance", "summary"]):
            self.valid_table = False
        elif any(word in title for word in ["credit", "deposit", "additions"]):
            self.valid_table = True

        if valid_date(date_str, "%m/%d") and self.valid_table and amount_str:
            try:
                amount = parse_amount(amount_str)
            except ValueError:
                return None

            if not valid_amount(amount):
                return None

            return Transaction.from_raw_data([date_str, description_str, amount])

        return None
