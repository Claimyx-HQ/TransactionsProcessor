from typing import Any, List
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class HancockWhitneyBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([55.5, 93.3, 161.7, 331.5, 368, 440, 606])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Transaction | None:
        title = ''.join(map(str, row[1:7])).upper()
        if any(title_type in title for title_type in ['DEBITS', 'DAILY BALANCE', 'SUMMARY']):
            self.valid_table = False
        if any(title_type in title for title_type in ['CREDIT', 'DEPOSIT', 'ADDITIONS']):
            self.valid_table = True
        
        for date_idx, amount_idx, description_idx in [(1, 2, 3), (4, 5, 6)]:
            date_str, amount_str, description_str = row[date_idx], row[amount_idx], row[description_idx]
            if valid_date(date_str, "%m/%d") and self.valid_table and amount_str:
                amount = parse_amount(amount_str)
                if valid_amount(amount):
                    return Transaction.from_raw_data([date_str, description_str, amount])
        
        return None
