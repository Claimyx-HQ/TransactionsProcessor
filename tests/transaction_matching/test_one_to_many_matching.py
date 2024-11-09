from pprint import pprint
from typing import List

from tests.mocks.transaction_matcher.multi_mock_transactions import (
    bank_transactions,
    system_transactions,
)
from transactions_processor.services.reconciliation.multi.default_multi_matcher import (
    DefaultMultiMatcher,
)


def test_find_one_to_many_matches():
    transaction_matcher = DefaultMultiMatcher()

    matches = transaction_matcher.find_one_to_many(
        bank_transactions, system_transactions
    )
