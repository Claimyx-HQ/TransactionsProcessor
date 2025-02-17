from typing import Dict, List

from tests.mocks.transaction_matcher.multi_mock_transactions import (
    bank_transactions,
    system_transactions,
)
from transactions_processor.schemas.transactions_matcher import ReconcilingMatches
from transactions_processor.services.reconciliation.multi.default_multi_matcher import (
    DefaultMultiMatcher,
)
from transactions_processor.services.reconciliation.utils.reconciliatoin_utils import (
    ReconciliationUtils,
)


def test_find_one_to_many_matches():
    transaction_matcher = DefaultMultiMatcher()

    matches = transaction_matcher.find_one_to_many(
        bank_transactions, system_transactions, 5
    )

    expected_dict = {
        100.0: [50.0, 50.0],
        709.9: [101.1, 101.25, 102.3, 103.15, 302.1],
        200.0: [80.0, 120.0],
        300.0: [300.0],
    }

    matched_values = _matched_to_values(matches)
    assert expected_dict == matched_values


def _matched_to_values(matched: ReconcilingMatches) -> Dict[float, List[float]]:
    matched_dict = {}
    for bank_group, system_group in matched.matched:
        bank_amount = bank_group[0].amount
        system_amounts = [transaction.amount for transaction in system_group]
        matched_dict[bank_amount] = system_amounts
    return matched_dict
