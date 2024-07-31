from typing import Any, List
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class MidFirstBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([75, 206, 281, 371, 441])

    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        date_str = str(row[0]).replace(' ', '')
        if valid_date(date_str, "%m-%d"):
            amount_str = str(row[2])
            subtraction_amount = str(row[3])
            description_str = row[1]
            if amount_str != "nan" and subtraction_amount == "nan":
                amount = parse_amount(amount_str)
                if valid_amount(amount):
                    return Transaction.from_raw_data([date_str, description_str, amount])
        return None
