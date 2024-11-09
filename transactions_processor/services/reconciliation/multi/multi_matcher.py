from abc import ABC, abstractmethod
from typing import List

from transactions_processor.schemas.transaction import Transaction
from transactions_processor.schemas.transactions_matcher import (
    ReconcilingMatches,
)


class MultiMatcher(ABC):

    @abstractmethod
    def find_one_to_many(
        self,
        bank_transactions: List[Transaction],
        system_transactions: List[Transaction],
    ) -> ReconcilingMatches:
        pass
