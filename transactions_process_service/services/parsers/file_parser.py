from abc import ABC, abstractmethod
from typing import Dict, List, Union

from transactions_process_service.schemas.transaction import Transaction


class FileParser(ABC):
    @abstractmethod
    def parse_transactions(self, file_path: str) -> List[Transaction]:
        raise NotImplementedError("parse_transactions method is not implemented")
