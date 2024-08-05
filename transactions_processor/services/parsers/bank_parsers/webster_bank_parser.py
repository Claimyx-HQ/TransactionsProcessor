from typing import Any, List, Union
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class WebsterBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([34, 120, 210, 300, 400, 490, 580, 670])
        self.valid_table = True

    def _parse_row(self, row: List[Any], table_index: int) -> Union[Transaction, None]:
        if len(row) == 7 and valid_date(row[1]) and self.valid_table:
            date_str, description_str, amount_str = row[1], row[2], row[5]
            if description_str == "Ending Balance":
                self.valid_table = False
                return None

            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data([date_str, description_str, amount])
        return None
