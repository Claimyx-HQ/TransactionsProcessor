from typing import BinaryIO, Dict, List, Union
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.parsers.bank_parsers.yad_bank_feeds_parser_csv import YadBankFeedsParserCSV
from transactions_processor.services.parsers.bank_parsers.yad_bank_feeds_parser_pdf import YadBankFeedsParserPDF
from transactions_processor.services.parsers.system_parsers.ncs.ncs_csv_parser import (
    NCSCSVParser,
)
from transactions_processor.services.parsers.system_parsers.ncs.ncs_pdf_parser import (
    NCSPDFParser,
)
from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)


class YadBankFeedsParser(TransactionsParser):
    def __init__(self) -> None:
        self.pdf_parser = YadBankFeedsParserPDF
        self.csv_parser = YadBankFeedsParserCSV

    def parse_transactions(
        self, file: BinaryIO, file_name: str | None, file_key: str | None = None
    ) -> List[Transaction]:
        file_extension = file_name.split(".")[-1] if file_name else None
        if not file_extension:
            raise ValueError("unknown file type")
        if file_extension.lower() == "pdf":
            return self.pdf_parser().parse_transactions(file, file_name, file_key)
        else:
            return self.csv_parser().parse_transactions(file, file_name, file_key)
