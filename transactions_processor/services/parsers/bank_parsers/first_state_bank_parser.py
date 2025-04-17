from typing import Any, List, Optional
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount
import pandas as pd
import re


class FirstStateBankParser(PDFParser):
    def __init__(self) -> None:
        super().__init__([118, 180, 826])
        self.in_credit_section = False
        self.found_credit_header = False

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:

        processed_row = " ".join(str(item)
                                 for item in row if pd.notna(item)).strip().upper()
        print(f"Processing row: {row}, Processed: {processed_row}")

        if "C O U N T C R E D I T T R A N S A C T I O N S" in processed_row:
            print("Found CREDIT transactions header")
            self.in_credit_section = True
            self.found_credit_header = True
            return None

        if "O T H E R D E B I T T R A N S A C T I O N S" in processed_row:
            print("Exiting CREDIT transactions section")
            self.in_credit_section = False
            return None

        if "DATE" in processed_row and "AMOUNT" in processed_row and "DESCRIPTION" in processed_row:
            print("Found table header, skipping")
            return None

        if self.in_credit_section and self.found_credit_header:

            date_candidate = str(row[0]).strip().split()[
                0] if pd.notna(row[0]) else ""
            print(f"Date candidate: {date_candidate}")

            date_clean = re.sub(r"[^\d/]", "", date_candidate)
            if valid_date(date_clean, "%m/%d"):
                print(f"Valid date found: {date_clean}")

                amount_candidate = None
                description_parts = []

                for i, cell in enumerate(row):
                    cell_str = str(cell).strip() if pd.notna(cell) else ""
                    if i == 1:

                        amount_clean = re.sub(r"[^\d.]", "", cell_str)
                        try:
                            amount = parse_amount(amount_clean)
                            if valid_amount(amount) and amount < 1_000_000:
                                amount_candidate = amount
                            else:
                                description_parts.append(cell_str)
                        except ValueError:
                            description_parts.append(cell_str)
                    elif i > 1:
                        description_parts.append(cell_str)

                if amount_candidate is not None:
                    description = " ".join(
                        part for part in description_parts if part).strip()
                    transaction = Transaction.from_raw_data(
                        date_clean, description, amount_candidate
                    )
                    print(f"Transaction created: {transaction}")
                    return transaction
                else:
                    print("Could not find valid amount in row")
                    return None
            else:
                print("Skipping row: Invalid or missing date")
                return None

        print("Row skipped: Not in credit section or invalid")
        return None
