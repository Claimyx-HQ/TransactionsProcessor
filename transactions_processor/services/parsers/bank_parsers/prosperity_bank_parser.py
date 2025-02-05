from typing import Any, List, Union
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class ProsperityBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([120, 490])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Union[Transaction, None]:
        section_title = str(row[0])
        if not self.valid_table:
            if section_title.startswith("DEPOSITS"):
                self.valid_table = True
        else:
            if section_title.startswith("OTHER"):
                self.valid_table = False
            date_str = row[0]
            if valid_date(date_str, "%d/%m/%Y") and self.valid_table:
                pass
                description_str, amount_str = row[1], row[2]
                amount = parse_amount(amount_str)
                if valid_amount(amount):
                    return Transaction.from_raw_data(date_str, description_str, amount)
        return None
