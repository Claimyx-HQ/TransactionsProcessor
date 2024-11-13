from collections.abc import Callable
from typing import List

from transactions_processor.schemas.transaction import Transaction
from transactions_processor.schemas.transactions_matcher import (
    MatchedTransactions,
    ReconcilingMatches,
)
from transactions_processor.services.reconciliation.mono.default_mono_matcher import (
    DefaultMonoMatcher,
)
from transactions_processor.services.reconciliation.multi.default_multi_matcher import (
    DefaultMultiMatcher,
)
from transactions_processor.services.reconciliation.utils.progress_callback import (
    ProgressCallback,
)


class TransactionsMatcher:

    def __init__(self):
        self._update_progress = ProgressCallback()
        self._mono_transaction_matcher = DefaultMonoMatcher()
        self._multi_transaction_matcher = DefaultMultiMatcher(self._update_progress)

    def set_update_progress(self, update_progress: Callable[[float], None]) -> None:
        self._update_progress.callback = update_progress

    def find_one_to_one_matches(
        self,
        bank_transactions: List[Transaction],
        system_transactions: List[Transaction],
    ) -> MatchedTransactions:
        matches = self._mono_transaction_matcher.find_one_to_one(
            bank_transactions, system_transactions
        )
        return matches

    def find_one_to_many_matches(
        self,
        bank_transactions: List[Transaction],
        system_transactions: List[Transaction],
        max_matches: int,
    ) -> ReconcilingMatches:
        matches = self._multi_transaction_matcher.find_one_to_many(
            bank_transactions, system_transactions, max_matches
        )
        return matches
