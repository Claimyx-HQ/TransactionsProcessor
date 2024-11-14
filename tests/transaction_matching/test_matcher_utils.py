from datetime import datetime
from typing import List
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.reconciliation.utils.reconciliatoin_utils import (
    ReconciliationUtils,
)
from transactions_processor.services.reconciliation.utils.transaction_utils import (
    TransactionUtils,
)
from tests.mocks.transaction_matcher.mock_transactions import (
    bank_transactions as mock_bank_transactions,
    system_transactions as mock_system_transactions,
)


def test_find_reconciliation_matches():
    bank_amount = 113
    system_amounts: List[float] = [50, 50, 120, 13, 80, 200, 300, 113]
    expected_matches = [[113], [50, 50, 13]]

    max_possibilities = 5
    possible_matches = []
    ReconciliationUtils.find_matches_n_sum(
        system_amounts,
        bank_amount,
        max_possibilities,
        0,
        [],
        possible_matches,
    )
    assert possible_matches == expected_matches


def test_match_amounts_to_transactions():
    bank_matches: Dict[float, List[float]] = {
        100: [50, 50],
    }
    system_matches = {}
    bank_transactions = [
        Transaction(
            date=datetime(2021, 1, 1),
            description="AAA",
            amount=transaction_amount,
            batch_number=i,
            origin="bank_file.csv",
        )
        for i, transaction_amount in enumerate(bank_matches.keys())
    ] + [
        Transaction(
            date=datetime(2021, 1, 1),
            description="BBB",
            amount=300,
            batch_number=3,
            origin="bank_file.csv",
        )
    ]

    system_transactions = [
        Transaction(
            date=datetime(2021, 1, 1),
            description="Automatic Transfer",
            amount=transaction_amount,
            batch_number=i,
            origin="system_file.xls",
        )
        for i, transaction_amount in enumerate([50, 50])
    ] + [
        Transaction(
            date=datetime(2021, 1, 1),
            description="Automatic Transfer",
            amount=300,
            batch_number=3,
            origin="system_file.xls",
        )
    ]
    matches = TransactionUtils.matched_amounts_to_transactions(
        bank_matches, system_matches, bank_transactions, system_transactions
    )

    expected_matched = [
        ([bank_transactions[0]], [system_transactions[1], system_transactions[0]]),
    ]
    expected_unmatched_bank = [bank_transactions[1]]
    expected_unmatched_system = [system_transactions[2]]

    assert matches.matched == expected_matched
    assert matches.unmatched_bank == expected_unmatched_bank
    assert matches.unmatched_system == expected_unmatched_system


def test_find_transaction_description_groups():
    grouped_transactions = ReconciliationUtils.group_by_description(
        mock_bank_transactions
    )
    exptected_groups = [
        [mock_bank_transactions[0], mock_bank_transactions[1]],
        [mock_bank_transactions[2], mock_bank_transactions[3]],
    ]
    assert grouped_transactions == exptected_groups
