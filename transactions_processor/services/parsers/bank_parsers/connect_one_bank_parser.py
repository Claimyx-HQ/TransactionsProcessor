from typing import Any, List, Optional
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class ConnectOneBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([109, 131.8, 443, 516.3])
        self.valid_table = True

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        row_type = str(row[0]).upper()
        if row_type == "DEBITS":
            self.valid_table = False
        elif row_type == "CREDITS":
            self.valid_table = True

        date_str = str(row[1])
        if valid_date(date_str, "%m-%d") and self.valid_table:
            amount_str = str(row[3])
            description_str = str(row[2])

            try:
                amount = parse_amount(amount_str)
                if not valid_amount(amount):
                    return None
            except ValueError:
                return None

            return Transaction.from_raw_data(date_str, description_str, amount)

        return None
