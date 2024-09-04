from typing import Any, List, Union
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class SunflowerBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([96, 460, 570])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Union[Transaction, None]:
        title = (str(row[0]) + str(row[1])).lower()
        self.valid_table = not any(
            title_type.lower() in title
            for title_type in [
                "debits",
                "daily",
                "balance",
                "summary",
                "electronic transactions",
            ]
        )
        if any(
            title_type.lower() in title
            for title_type in ["credit", "deposit", "additions"]
        ):
            self.valid_table = True

        date_str, description_str, amount_str = row[0], row[1], row[2]
        if valid_date(date_str, "%m/%d/%y") and self.valid_table and amount_str:
            amount = parse_amount(amount_str)
            if valid_amount(amount) and amount >= 0:
                return Transaction.from_raw_data(date_str, description_str, amount)
        return None
