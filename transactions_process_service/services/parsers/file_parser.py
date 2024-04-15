from abc import ABC, abstractmethod
from typing import Dict, List, Union

from starlette.datastructures import UploadFile

from transactions_process_service.schemas.transaction import Transaction


class FileParser(ABC):
    @abstractmethod
    def parse_transactions(self, file: UploadFile) -> List[Transaction]:
        raise NotImplementedError("parse_transactions method is not implemented")
