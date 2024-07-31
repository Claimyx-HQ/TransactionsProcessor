from typing import Any, List, Optional
from transactions_processor.models.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class CustomersBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([50, 115, 470, 570])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        title = ' '.join(str(cell) for cell in row[:3]).lower()
        if any(keyword in title for keyword in ['withdrawal', 'debits', 'daily', 'balance', 'summary', 'fee']):
            self.valid_table = False
        elif 'credits' in title:
            self.valid_table = True

        date_str = str(row[1])
        amount_str = str(row[3])
        description_str = str(row[2])

        if valid_date(date_str, "%m/%d/%Y") and self.valid_table and amount_str:
            try:
                amount = parse_amount(amount_str)
                if not valid_amount(amount) or amount < 0:
                    return None
            except ValueError:
                return None

            return Transaction.from_raw_data([date_str, description_str, amount])

        return None
