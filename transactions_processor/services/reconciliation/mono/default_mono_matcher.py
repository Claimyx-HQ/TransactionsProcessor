from typing import List, Tuple

from transactions_processor.schemas.transaction import Transaction
from transactions_processor.schemas.transactions_matcher import MatchedTransactions
from transactions_processor.services.reconciliation.mono.mono_matcher import MonoMatcher


class DefaultMonoMatcher(MonoMatcher):
    def __init__(self):
        pass

    def find_one_to_one(
        self,
        bank_transactions: List[Transaction],
        system_transactions: List[Transaction],
    ) -> MatchedTransactions:
        matches: List[Tuple[Transaction, Transaction]] = []
        unmatched_bank_amounts: List[Transaction] = []
        unmatched_system_amounts: List[Transaction] = []
        bank_amounts = {}
        system_amounts = {}
        matched_amounts = set()

        # Create a dictionary of transactions grouped by amount
        for transaction in bank_transactions:
            if transaction.amount not in bank_amounts:
                bank_amounts[transaction.amount] = []
            bank_amounts[transaction.amount].append(transaction)

        for transaction in system_transactions:
            if transaction.amount not in system_amounts:
                system_amounts[transaction.amount] = []
            system_amounts[transaction.amount].append(transaction)

        for amount in bank_amounts:
            if amount in system_amounts:
                if len(bank_amounts[amount]) >= len(system_amounts[amount]):
                    unmatched_amounts_count = len(bank_amounts[amount]) - len(
                        system_amounts[amount]
                    )
                    for _ in range(unmatched_amounts_count):
                        unmatched_bank_amounts.append(bank_amounts[amount].pop())
                    for _ in range(len(system_amounts[amount])):
                        matches.append(
                            (bank_amounts[amount].pop(), system_amounts[amount].pop())
                        )
                elif len(bank_amounts[amount]) < len(system_amounts[amount]):
                    unmatched_amounts_count = len(system_amounts[amount]) - len(
                        bank_amounts[amount]
                    )
                    for _ in range(unmatched_amounts_count):
                        unmatched_system_amounts.append(system_amounts[amount].pop())
                    for _ in range(len(bank_amounts[amount])):
                        matches.append(
                            (bank_amounts[amount].pop(), system_amounts[amount].pop())
                        )
            else:
                for _ in range(len(bank_amounts[amount])):
                    unmatched_bank_amounts.append(bank_amounts[amount].pop())
            matched_amounts.add(amount)

        for amount in system_amounts:
            if amount not in matched_amounts:
                for _ in range(len(system_amounts[amount])):
                    unmatched_system_amounts.append(system_amounts[amount].pop())

        return MatchedTransactions(
            matched=matches,
            unmatched_bank=unmatched_bank_amounts,
            unmatched_system=unmatched_system_amounts,
        )
