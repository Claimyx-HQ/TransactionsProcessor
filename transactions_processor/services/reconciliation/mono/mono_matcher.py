from abc import ABC, abstractmethod
from typing import List

from transactions_processor.schemas.transaction import Transaction
from transactions_processor.schemas.transactions_matcher import MatchedTransactions


class MonoMatcher(ABC):

    @abstractmethod
    def find_one_to_one(
        self,
        bank_transactions: List[Transaction],
        system_transactions: List[Transaction],
    ) -> MatchedTransactions:
        pass
