from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, List, Union

from transactions_processor.models.transaction import Transaction


class TransactionsParser(ABC):
    @abstractmethod
    def parse_transactions(self, file: BinaryIO) -> List[Transaction]:
        raise NotImplementedError("parse_transactions method is not implemented")
