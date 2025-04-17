from typing import Any, List, Optional
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount


class SnbBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([108, 310, 440])
        self.valid_table = False

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        print("------------------------------------------------------------")
        print(f"Parsing row from table index {table_index}: {row}")

        date_str = str(row[0])
        description_str = str(row[1])
        amount_str = str(row[2])
        title = (date_str + description_str).lower()

        print(f"Title for keyword check: {title}")
        print(f"Raw date string: {date_str}")
        print(f"Raw description string: {description_str}")
        print(f"Raw amount string: {amount_str}")

        if any(keyword in title for keyword in ["debits", "daily balance", "summary"]):
            print("Table marked as invalid (contains exclusion keywords).")
            self.valid_table = False
        elif any(keyword in title for keyword in ['post date', 'description', 'debits', 'credits', 'balance']):
            print("Table marked as valid (contains inclusion keywords).")
            self.valid_table = True

        is_valid_date = valid_date(date_str, "%d/%m/%y")
        if not is_valid_date:
            print(f"Invalid date format: {date_str}")
        else:
            print(f"Valid date format: {date_str}")

        if not amount_str:
            print("Empty amount string.")
        else:
            print("Amount string exists.")

        if is_valid_date and self.valid_table and amount_str:
            try:
                amount = parse_amount(amount_str)
                print(f"Parsed amount: {amount}")

                if not valid_amount(amount):
                    print(f"Invalid amount (filtered out): {amount}")
                    return None
            except ValueError as e:
                print(f"Failed to parse amount: {amount_str} — Error: {e}")
                return None

            transaction = Transaction.from_raw_data(
                date_str, description_str, amount)
            print(f"Transaction created: {transaction}")
            return transaction

        print("ℹRow skipped due to failing validation checks.")
        return None
