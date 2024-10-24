from typing import Any, List, Optional
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount
from datetime import datetime


class FlagstarBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([80, 504, 576])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        date_str = str(row[0])
        description_str = str(row[1])
        amount_str = str(row[2])

        if date_str == "Deposits":
            self.valid_table = True
        elif date_str == "Withdraw":
            self.valid_table = False
            return None

        if valid_date(date_str, "%b %d") and self.valid_table:
            try:
                formatted_date = datetime.strptime(date_str, "%b %d").strftime("%m/%d")
                amount = parse_amount(amount_str)
                if not valid_amount(amount):
                    return None
            except ValueError:
                return None

            return Transaction.from_raw_data(formatted_date, description_str, amount)

        return None
