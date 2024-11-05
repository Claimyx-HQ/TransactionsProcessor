from typing import Any, List, Union
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class FortisBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([80, 300, 370, 510])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Union[Transaction, None]:
        print(row)
        date_str, description_str, amount_str = row[0], row[1], row[2]
        title = (str(date_str)+str(description_str)+str(amount_str)).upper()
        if any(
            title_type in title
            for title_type in ["WITHDRAWAL", "DAILY BALANCE", "SUMMARY"]
        ):
            self.valid_table = False
        elif any(
            title_type in title
            for title_type in ["DEPOSITS","CREDITS"]
        ):
            self.valid_table = True
        date_str = date_str.replace(" ", "")
        if valid_date(date_str, "%m/%d") and self.valid_table and amount_str:
            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data(date_str, description_str, amount)
        return None
