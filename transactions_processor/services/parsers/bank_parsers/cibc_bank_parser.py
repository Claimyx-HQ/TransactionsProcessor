from typing import Any, List, Optional
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class CIBCBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([50, 100, 300])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        second_col_str = str(row[1]).lower()

        if "credits" in second_col_str:
            self.valid_table = True
        elif "daily" in second_col_str:
            self.valid_table = False
            return None

        if self.valid_table and valid_date(second_col_str, "%m/%d"):
            date_str = second_col_str
            description_str = str(row[2])
            amount_str = str(row[3])

            try:
                amount = parse_amount(amount_str)
            except ValueError:
                return None

            if not valid_amount(amount):
                return None

            return Transaction.from_raw_data(date_str, description_str, amount)

        return None
