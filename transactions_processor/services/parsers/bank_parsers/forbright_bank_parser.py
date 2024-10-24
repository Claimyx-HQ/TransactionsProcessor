from typing import Any, List, Optional
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class ForbrightBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([50, 150, 400])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        date_str = str(row[1])
        title = date_str.upper()
        description_str = str(row[2])
        amount_str = str(row[3])

        if title == "CREDITS":
            self.valid_table = True
        elif title == "DAILY BALANCES":
            self.valid_table = False

        if valid_date(date_str, "%m-%d") and self.valid_table:
            try:
                amount = parse_amount(amount_str)
                if not valid_amount(amount):
                    return None
            except ValueError:
                return None

            return Transaction.from_raw_data(date_str, description_str, amount)

        return None
