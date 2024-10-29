from typing import BinaryIO, List
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.csv_parser import CSVParser

class WorkdayBankFeedsParser(CSVParser):
    def __init__(self) -> None:
        super().__init__(
            date_col_index=5,         
            description_col_indx=11,    
            amount_col_index=7,         
            batch_col_index=3          
        )
        self.debit_credit_col_index = 8 

    def parse_transactions(
        self,
        file: BinaryIO,
        file_name: str | None = None,
        file_key: str | None = None,
    ) -> List[Transaction]:
        self.file_name = file_name

        # Parse the file into a DataFrame
        df = self._parse_excel(file)

        # Select relevant columns including Debit/Credit for filtering
        column_indexes = [
            self.date_col_index,
            self.description_col_indx,
            self.amount_col_index,
            self.batch_col_index,
            self.debit_credit_col_index,  # Include for filtering
        ]

        # Extract important columns
        important_columns = df.iloc[:, column_indexes]

        # Filter rows where Debit/Credit is 'CR'
        # Assuming 'CR' indicates credits
        important_columns = important_columns[
            important_columns.iloc[:, -1].str.strip().str.upper() == 'CR'
        ]

        # Remove the Debit/Credit column as it's no longer needed
        important_columns = important_columns.iloc[:, :-1]

        # Drop rows with missing values
        important_columns = important_columns.dropna()

        # Create Transaction objects
        transactions: List[Transaction] = []
        for row in important_columns.itertuples(index=False):
            transaction = Transaction.from_raw_data(*row, origin=file_name)
            transactions.append(transaction)

        return transactions
