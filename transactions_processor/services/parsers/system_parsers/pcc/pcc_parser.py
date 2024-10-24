import logging
import math
from typing import BinaryIO, Dict, List, Union
import tabula
import pandas as pd
import numpy as np
import re
from transactions_processor.schemas.transaction import Transaction
from datetime import datetime

from transactions_processor.services.parsers.system_parsers.pcc.pcc_csv_parser import (
    PCCCSVParser,
)
from transactions_processor.services.parsers.system_parsers.pcc.pcc_pdf_parser import (
    PCCPDFParser,
)
from transactions_processor.services.parsers.transactions_parser import (
    TransactionsParser,
)
from transactions_processor.utils.math_utils import parse_amount


class PCCParser(TransactionsParser):
    def __init__(self) -> None:
        self.pdf_parser = PCCPDFParser
        self.csv_parser = PCCCSVParser
        self.decoded_data = []
        self.formated_data = []
        self.logger = logging.getLogger(__name__)

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
