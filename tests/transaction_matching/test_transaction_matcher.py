from typing import List
from transactions_process_service.schemas.transaction import Transaction
from transactions_process_service.services.transaction_matcher import (
    TransactionMathcher,
)


def test_find_matches():
    transaction_matcher = TransactionMathcher()
    bank_amounts: List[float] = [100, 200, 300]
    system_amounts: List[float] = [100, 200, 400]
    expected_matched = [100, 200]
    expected_unmatched = [300]

    matched, unmatched = transaction_matcher.find_matched_unmatched(
        bank_amounts, system_amounts
    )

    assert matched == expected_matched
    assert unmatched == expected_unmatched


def test_find_reconciling_matches():
    transaction_matcher = TransactionMathcher()
    bank_amounts: List[float] = [100, 200, 300]
    system_amounts: List[float] = [50, 50, 120, 80, 200]
    expected_matches = {
        100: [50, 50],
        200: [200],
    }

    matches = transaction_matcher.find_reconciling_matches(bank_amounts, system_amounts)

    assert matches == expected_matches
