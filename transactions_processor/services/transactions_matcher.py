from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Dict, List, Tuple


class TransactionsMatcher(ABC):

    @abstractmethod
    def find_matched_unmatched(
        self, bank_transactions: List[float], system_transactions: List[float]
    ) -> Tuple[list[float], list[float], list[float]]:
        pass

    @abstractmethod
    def find_reconciling_matches(
        self,
        bank_transactions: List[float],
        system_transactions: List[float],
        update_progress: Callable[[float], None] | None = None,
    ) -> Tuple[Dict[float, List[float]], List[float], List[float]]:
        pass
