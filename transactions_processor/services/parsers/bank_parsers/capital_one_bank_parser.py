from typing import Any, List, Union
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class CapitalOneBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([75, 300, 400, 450])
        self.valid_table = True

    def _parse_row(self, row: List[Any], table_index: int) -> Union[Transaction, None]:
        row_parts = row[0].split(" ")
        date_str = row_parts[0]
        if valid_date(date_str, "%m/%d"):
            description_first_part = row_parts[1] if len(row_parts) > 1 else ""
            description_second_part = row[1]
            description_str = f"{description_first_part}{description_second_part}"
            amount_str = row[2].split(" ")[0]
            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data(date_str, description_str, amount)
        return None
