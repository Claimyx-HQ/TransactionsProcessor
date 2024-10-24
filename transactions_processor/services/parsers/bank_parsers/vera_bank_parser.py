from typing import Any, List, Union
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount
from datetime import datetime


class VeraBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([43, 79, 519, 574])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Union[Transaction, None]:
        date_str, description_str, amount_str = str(row[1]), str(row[2]), str(row[3])
        title = (date_str + description_str).lower()

        if any(title_type in title for title_type in ["debit", "balance", "summary"]):
            self.valid_table = False
        if "credits" in title:
            self.valid_table = True

        if valid_date(date_str, "%b %d") and self.valid_table and amount_str:
            date_str = datetime.strptime(date_str, "%b %d").strftime("%m/%d")
            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data(date_str, description_str, amount)
        return None
