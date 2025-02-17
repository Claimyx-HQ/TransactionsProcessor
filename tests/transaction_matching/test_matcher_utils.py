import pytest
from datetime import datetime
from typing import Dict, List
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

test_cases = {
    "case1": {
        "bank_amount": 113,
        "system_amounts": [
            50.1,
            50.32,
            120.22,
            13.01,
            80.3,
            50.1,
            50.32,
            120.22,
            13.01,
            80.3,
            50.1,
            50.32,
            120.22,
            13.01,
            80.3,
            50.1,
            50.32,
            120.22,
            13.01,
            80.3,
            50,
            50,
            120,
            13,
            80,
            200,
            300,
            113,
        ],
        "max_possibilities": 20,
        "expected": [[13, 50, 50], [113]],
    },
    "case2": {
        "bank_amount": 709.9,
        "system_amounts": [101.1, 101.25, 102.3, 103.15, 302.1],
        "max_possibilities": 5,
        "expected": [[101.1, 101.25, 102.3, 103.15, 302.1]],
    },
    "case3": {
        "bank_amount": 709.9,
        "system_amounts": [
            2.74,
            2.66,
            3.14,
            1.07,
            1.76,
            3.32,
            3.5,
            1.44,
            3.01,
            1.48,
            2.69,
            2.92,
            2.76,
            3.24,
            3.15,
            2.62,
            1.8,
            2.58,
            3.02,
            1.55,
            2.97,
            3.43,
            1.16,
            2.32,
            3.17,
            2.72,
            3.44,
            1.56,
            2.21,
            1.04,
            1.4,
            1.29,
            2.41,
            2.66,
            2.91,
            3.65,
            2.6,
            3.6,
            2.53,
            2.44,
            2.83,
            2.3,
            2.79,
            1.4,
            2.08,
            1.37,
            2.61,
            1.69,
            2.21,
            1.95,
            1.21,
            1.71,
            1.93,
            2.04,
            1.93,
            3.21,
            3.34,
            2.37,
            2.02,
            2.11,
            2.27,
            3.24,
            3.49,
            1.1,
            3.68,
            3.89,
            2.66,
            3.44,
            2.35,
            1.44,
            1.27,
            3.71,
            1.12,
            1.46,
            3.34,
            3.23,
            1.5,
            1.2,
            3.85,
            1.68,
            3.52,
            1.23,
            3.12,
            2.57,
            1.58,
            3.73,
            2.43,
            3.54,
            1.74,
            3.28,
            4.33,
            2.62,
            4.2,
            3.33,
            1.94,
            2.75,
            1.86,
            2.53,
            2.0,
            3.47,
            1.26,
            3.95,
            4.31,
            2.93,
            1.64,
            4.47,
            2.81,
            3.79,
            4.56,
            3.78,
            1.85,
            2.69,
            4.11,
            3.57,
            2.91,
            1.38,
            3.06,
            2.56,
            4.1,
            4.24,
            3.06,
            1.02,
            1.56,
            4.25,
            1.22,
            3.53,
            4.58,
            2.25,
            1.11,
            3.23,
            4.6,
            4.64,
            1.3,
            5.17,
            1.33,
            2.85,
            3.49,
            4.88,
            4.32,
            1.13,
            3.05,
            3.99,
            5.0,
            2.57,
            1.63,
            5.82,
            2.52,
            3.83,
            2.02,
            3.78,
            5.3,
            1.14,
            3.09,
            5.92,
            3.18,
            2.98,
            4.77,
            5.41,
            3.07,
            2.73,
            4.19,
            5.4,
            6.14,
            6.72,
            5.64,
            2.17,
            5.56,
            3.3,
            6.15,
            4.72,
            3.44,
            5.69,
            3.68,
            3.87,
            1.65,
            6.32,
            5.61,
            7.04,
            5.35,
            1.69,
            5.29,
            4.71,
            8.06,
            8.62,
            4.86,
            1.09,
            3.84,
            3.93,
            4.2,
            4.55,
            5.23,
            5.42,
            3.97,
            3.33,
            6.74,
            19.26,
            5.45,
            7.89,
            12.31,
            52.78,
        ],
        "expected": [],
        "max_possibilities": 4,
    },
}


@pytest.mark.parametrize("data", test_cases.values(), ids=test_cases.keys())
def test_find_reconciliation_matches(data):
    bank_amount = data["bank_amount"]
    system_amounts: List[float] = data["system_amounts"]
    expected_matches = data["expected"]

    max_possibilities = data["max_possibilities"]
    possible_matches = []
    # ReconciliationUtils.find_matches_n_sum(
    #     system_amounts,
    #     bank_amount,
    #     max_possibilities,
    #     0,
    #     [],
    #     possible_matches,
    # )

    possible_matches = ReconciliationUtils.find_matches_n_sum2(
        system_amounts,
        bank_amount,
        max_elements=max_possibilities,
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
