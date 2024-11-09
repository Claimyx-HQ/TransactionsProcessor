from typing import Any, Dict, List

from transactions_processor.schemas.transaction import Transaction
from transactions_processor.schemas.transactions_matcher import ReconcilingMatches


class TransactionUtils:

    @staticmethod
    def matched_amounts_to_transactions(
        bank_matches: Dict[float, List[float]],
        system_matches: Dict[float, List[float]],
        bank_transactions: List[Transaction],
        system_transactions: List[Transaction],
    ) -> ReconcilingMatches:
        result = ReconcilingMatches(
            matched=[],
            unmatched_bank=[],
            unmatched_system=[],
        )
        bank_transactions_map = {}
        system_transactions_map = {}
        for transaction in bank_transactions:
            bank_transactions_map[transaction.amount] = bank_transactions_map.get(
                transaction.amount, []
            )
            bank_transactions_map[transaction.amount].append(transaction)
        for transaction in system_transactions:
            system_transactions_map[transaction.amount] = system_transactions_map.get(
                transaction.amount, []
            )
            system_transactions_map[transaction.amount].append(transaction)

        for amount in bank_matches.keys():
            bank_transaction = bank_transactions_map[amount].pop()
            if len(bank_transactions_map[amount]) == 0:
                del bank_transactions_map[amount]
            matched_transactions = []
            for matched_amount in bank_matches[amount]:
                system_transaction = system_transactions_map[matched_amount].pop()
                if len(system_transactions_map[matched_amount]) == 0:
                    del system_transactions_map[matched_amount]
                matched_transactions.append(system_transaction)
            result.matched.append(
                (
                    [bank_transaction],
                    matched_transactions,
                )
            )

        for amount in system_matches.keys():
            system_transaction = system_transactions_map[amount].pop()
            if len(system_transactions_map[amount]) == 0:
                del system_transactions_map[amount]
            matched_transactions = []
            for matched_amount in system_matches[amount]:
                bank_transaction = bank_transactions_map[matched_amount].pop()
                if len(bank_transactions_map[matched_amount]) == 0:
                    del bank_transactions_map[matched_amount]
                matched_transactions.append(bank_transaction)
            result.matched.append(
                (
                    matched_transactions,
                    [system_transaction],
                )
            )

        for amount in bank_transactions_map.keys():
            result.unmatched_bank.extend(bank_transactions_map[amount])

        for amount in system_transactions_map.keys():
            result.unmatched_system.extend(system_transactions_map[amount])

        return result
