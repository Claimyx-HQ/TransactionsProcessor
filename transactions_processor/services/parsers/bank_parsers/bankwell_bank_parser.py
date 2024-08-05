from typing import Any, List, Optional
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class BankWellBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([87, 320, 410, 485, 570])

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        date_str = str(row[0]).replace(" ", "")
        if not valid_date(date_str, "%m/%d/%Y"):
            return None

        description_str = str(row[1])
        amount_str = str(row[3])
        subtraction_amount = str(row[2])

        if subtraction_amount != "nan":
            try:
                subtraction_amount = parse_amount(subtraction_amount)
            except ValueError:
                return None

        if amount_str != "nan" and (
            subtraction_amount == 0 or subtraction_amount == "nan"
        ):
            try:
                amount = parse_amount(amount_str)
            except ValueError:
                return None
            if not valid_amount(amount):
                return None
            return Transaction.from_raw_data([date_str, description_str, amount])

        return None
