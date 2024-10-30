from typing import Any, List, Optional
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class CfgBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([92, 432, 573])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        date_str = str(row[0])
        description_str = str(row[1])
        amount_str = str(row[2])

        title = (date_str + description_str).lower()
        if any(
            title_type in title
            for title_type in ["electronic debits", "daily balance", "other debits"]
        ):
            self.valid_table = False
        elif any(
            title_type in title
            for title_type in ["deposits", "electronic credits"]
        ):
            self.valid_table = True

        if valid_date(date_str, "%m/%d/%Y") and self.valid_table:
            try:
                amount = parse_amount(amount_str)
            except ValueError:
                return None

            if not valid_amount(amount):
                return None

            return Transaction.from_raw_data(date_str, description_str, amount)

        return None
