from typing import Any, List
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class OldNationalBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([55, 105, 210, 450, 560])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        date_str = str(row[1]).replace(" ", "")
        description_str = row[3]
        title = (str(date_str) + str(description_str)).lower()
        amount_str = row[4]

        if any(
            title_type in title
            for title_type in [
                "fee",
                "debits",
                "daily balance",
                "summary",
                "withdrawals",
            ]
        ):
            self.valid_table = False
        elif any(
            title_type in title for title_type in ["credit", "deposit", "additions"]
        ):
            self.valid_table = True

        if valid_date(date_str, "%m/%d") and self.valid_table and amount_str:
            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data(date_str, description_str, amount)
        return None
