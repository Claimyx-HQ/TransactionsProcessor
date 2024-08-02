from typing import Any, List, Union
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount
from datetime import datetime


class VistaBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([55, 92, 351, 423, 504, 565])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Union[Transaction, None]:
        date_str, description_str, amount_str = str(row[1]), str(row[2]), row[3]
        title = (date_str + description_str).lower()

        if any(title_type.lower() in title for title_type in ['fee', 'debit', 'summary']):
            self.valid_table = False
        if 'transaction detail' in title:
            self.valid_table = True

        if valid_date(date_str, "%b %d") and self.valid_table and amount_str:
            date_str = datetime.strptime(date_str, '%b %d').strftime('%m/%d')
            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data([date_str, description_str, amount])
        return None
