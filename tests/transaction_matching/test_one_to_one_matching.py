from typing import List

from tests.mocks.transaction_matcher.mock_transactions import (
    bank_transactions,
    system_transactions,
)
from transactions_processor.services.reconciliation.mono.default_mono_matcher import (
    DefaultMonoMatcher,
)


def test_find_one_to_one_matches():
    transaction_matcher = DefaultMonoMatcher()

    exected_matched = [
        (bank_transactions[0], system_transactions[0]),
        (bank_transactions[1], system_transactions[1]),
        (bank_transactions[3], system_transactions[2]),
    ]
    exptected_unmatched_bank = [bank_transactions[2], bank_transactions[4]]
    exptected_unmatched_system = [system_transactions[3], system_transactions[4]]

    matched_transactions = transaction_matcher.find_one_to_one(
        bank_transactions, system_transactions
    )
    assert matched_transactions.matched == exected_matched
    assert matched_transactions.unmatched_bank == exptected_unmatched_bank
    assert matched_transactions.unmatched_system == exptected_unmatched_system
