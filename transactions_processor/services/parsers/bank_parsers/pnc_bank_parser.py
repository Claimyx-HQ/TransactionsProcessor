from typing import Any, List, Union
from transactions_processor.models.transaction import Transaction

from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class PNCBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([90, 300, 360, 420, 600])

    def _parse_row(self, row: List[Any], table_index: int) -> Union[Transaction, None]:
        if valid_date(row[0]):
            date_str, description_str, amount_str = row[0], row[1], row[3]
            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data([date_str, description_str, amount])
        return None
