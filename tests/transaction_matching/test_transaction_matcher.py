import time
from typing import List
import pprint

from tests.mocks.transaction_matcher.mock_transactions import (
    bank_transactions,
    system_transactions,
)


# def test_find_matches():
#     transaction_matcher = SingleTransactionsMatcher()
#
#     exected_matched = [
#         (bank_transactions[0], system_transactions[0]),
#         (bank_transactions[1], system_transactions[1]),
#         (bank_transactions[3], system_transactions[2]),
#     ]
#     exptected_unmatched_bank = [bank_transactions[2], bank_transactions[4]]
#     exptected_unmatched_system = [system_transactions[3], system_transactions[4]]
#
#     matched_transactions = transaction_matcher.find_one_to_one_matches(
#         bank_transactions, system_transactions
#     )
#     assert matched_transactions.matched == exected_matched
#     assert matched_transactions.unmatched_bank == exptected_unmatched_bank
#     assert matched_transactions.unmatched_system == exptected_unmatched_system


# def test_find_reconciling_matches():
#     transaction_matcher = ParallelTransactionsMatcher()
#     bank_amounts: List[float] = [100, 200, 300, 300]
#     system_amounts: List[float] = [50, 50, 120, 80, 200, 300]
#     expected_matches = {
#         100: [50, 50],
#         200: [200],
#         300: [300],
#     }
#     expected_bank_unmatched = [300]
#     expected_system_unmatched = [120, 80]
#
#     (
#         matches,
#         unmatched_bank_amounts,
#         unmatched_system_amounts,
#     ) = transaction_matcher.find_reconciling_matches(bank_amounts, system_amounts)
#
#     assert matches == expected_matches
#     assert unmatched_bank_amounts == expected_bank_unmatched
#     assert unmatched_system_amounts == expected_system_unmatched
#
#
# def test_find_transaction_description_groups():
#     transaction_matcher = ParallelTransactionsMatcher()
#     grouped_transactions = transaction_matcher.group_by_description(bank_transactions)
#     exptected_groups = [
#         [bank_transactions[0], bank_transactions[1]],
#         [bank_transactions[2], bank_transactions[3]],
#     ]
#     assert grouped_transactions == exptected_groups
