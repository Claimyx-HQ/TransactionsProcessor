from typing import Any, List, Union
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class SimmonsBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([70, 260, 430])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Union[Transaction, None]:
        date_str = str(row[0]).replace(" ", "")
        description_str = str(row[1])
        amount_str = str(row[2])

        title = (date_str + description_str).lower()
        if any(
            title_type in title
            for title_type in ["debits", "daily balance", "withdrawals"]
        ):
            self.valid_table = False
        if any(title_type in title for title_type in ["credit", "additions"]):
            self.valid_table = True
        if valid_date(date_str, "%m/%d") and self.valid_table and amount_str:
            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data([date_str, description_str, amount])
        return None
