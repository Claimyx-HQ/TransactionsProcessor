from typing import List
from transactions_process_service.schemas.transaction import Transaction
from transactions_process_service.services.transaction_matcher import (
    TransactionMathcher,
)


# TODO: Handle duplicates
def test_find_matches():
    transaction_matcher = TransactionMathcher()
    bank_amounts: List[float] = [100, 200, 300]
    system_amounts: List[float] = [100, 200, 400]
    expected_matched = [200, 100]
    expected_unmatched_bank_amounts = [300]
    expected_unmatched_system_amounts = [400]

    (
        matched,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_matched_unmatched(bank_amounts, system_amounts)

    assert matched == expected_matched
    assert unmatched_bank_amounts == expected_unmatched_bank_amounts
    assert unmatched_system_amounts == expected_unmatched_system_amounts


def test_find_reconciling_matches():
    transaction_matcher = TransactionMathcher()
    bank_amounts: List[float] = [100, 200, 300, 300]
    system_amounts: List[float] = [50, 50, 120, 80, 200, 300]
    expected_matches = {
        100: [50, 50],
        200: [200],
        300: [300],
    }
    expected_bank_unmatched = [300]
    expected_system_unmatched = [120, 80]

    (
        matches,
        unmatched_bank_amounts,
        unmatched_system_amounts,
    ) = transaction_matcher.find_reconciling_matches(bank_amounts, system_amounts)

    assert matches == expected_matches
    assert unmatched_bank_amounts == expected_bank_unmatched
    assert unmatched_system_amounts == expected_system_unmatched
