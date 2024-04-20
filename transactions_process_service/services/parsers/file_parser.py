from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, List, Union

from starlette.datastructures import UploadFile

from transactions_process_service.schemas.transaction import Transaction


class FileParser(ABC):
    @abstractmethod
    def parse_transactions(self, file: BinaryIO) -> List[Transaction]:
        raise NotImplementedError("parse_transactions method is not implemented")
