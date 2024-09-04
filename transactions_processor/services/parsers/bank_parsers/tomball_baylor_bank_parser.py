from typing import Any, List, Union
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class TomballBaylorBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([100, 300])
        self.valid_table = True

    def _parse_row(self, row: List[Any], table_index: int) -> Union[Transaction, None]:
        if row[0] == "OTHER D":
            self._enable = False
            return None

        date_str, description_str, amount_str = row[0], row[1], row[2]

        if valid_date(date_str, "%m/%d"):
            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data(date_str, description_str, amount)
        return None
