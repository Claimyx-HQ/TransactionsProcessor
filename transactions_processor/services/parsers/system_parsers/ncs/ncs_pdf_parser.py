from typing import Any, List, Optional
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class NCSPDFParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([62, 142, 195, 295, 500])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        date_str = row[0]
        if valid_date(date_str, "%m/%d/%y"):
            amount_str = row[3]
            description_str = row[4]

            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data(date_str, description_str, amount)
        return None
