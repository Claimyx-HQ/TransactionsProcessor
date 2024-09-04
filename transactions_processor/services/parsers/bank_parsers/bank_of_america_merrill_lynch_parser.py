from typing import Any, List, Optional
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class BankOfAmericaMerrillLynchParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([62, 122, 202, 544, 616])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        title = "".join(map(str, row[:4])).replace("_", "").lower()
        if any(word in title for word in ["debits", "daily", "balance", "summary"]):
            self.valid_table = False
        elif any(word in title for word in ["credit", "deposit", "additions"]):
            self.valid_table = True

        date_str, amount_str, description_str = row[0], row[2], row[3]

        if valid_date(date_str, "%m/%d") and self.valid_table and amount_str:
            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data(date_str, description_str, amount)

        return None
