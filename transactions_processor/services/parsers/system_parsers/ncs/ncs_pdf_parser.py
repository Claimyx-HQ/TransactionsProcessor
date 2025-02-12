from typing import Any, BinaryIO, List, Optional
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.pdf_parser import PDFParser
from transactions_processor.utils.date_utils import valid_date
from transactions_processor.utils.math_utils import parse_amount, valid_amount
import tabula

VERSION_1_COULMN_POSITIONS: List[float] = [62, 142, 195, 295, 500]
VERSION_2_COULMN_POSITIONS: List[float] = [62, 142, 210, 500]


class NCSPDFParser(PDFParser):
    def __init__(self) -> None:
        super().__init__(VERSION_1_COULMN_POSITIONS)

    def parse_transactions(
        self,
        file: BinaryIO,
        file_name: str | None = None,
        file_key: str | None = None,
    ) -> List[Transaction]:
        self.file_name = file_name
        pdf_header_data = self._parse_pdf_header(file)
        self.pdf_version = self._identify_pdf_version(pdf_header_data)
        if self.pdf_version == 1:
            self.column_positions = VERSION_1_COULMN_POSITIONS
        else:
            self.column_positions = VERSION_2_COULMN_POSITIONS
        return super().parse_transactions(file, file_name, file_key)

    def _parse_pdf_header(self, file: BinaryIO) -> List:
        tables = tabula.io.read_pdf(
            file,
            multiple_tables=True,
            pages="1",
            pandas_options={"header": None},
            guess=False,
            area=[0, 0, 100, 100],
        )
        if len(tables) == 0:
            raise ValueError("No tables found in PDF")

        table_data: List = tables[0].values.tolist()  # type: ignore
        rows = [row[0] for row in table_data]
        return rows

    def _identify_pdf_version(self, rows: List) -> int:
        if "Date Bank" in rows:
            return 1
        return 2

    def _parse_row(self, row: List[Any], table_index: int) -> Optional[Transaction]:
        date_str = row[0]
        if valid_date(date_str, "%m/%d/%y"):
            amount_str = row[3] if self.pdf_version == 1 else row[2]
            description_str = row[4] if self.pdf_version == 1 else row[3]
            batch_number = row[5] if self.pdf_version == 1 else row[4]

            amount = parse_amount(amount_str)
            if valid_amount(amount):
                return Transaction.from_raw_data(
                    date_str, description_str, amount, batch_number
                )
        return None
