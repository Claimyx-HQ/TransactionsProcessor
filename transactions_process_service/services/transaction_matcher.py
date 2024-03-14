import logging
from typing import Any, Dict, List, Tuple
import numpy as np


class TransactionMathcher:
    # Return matching and unmatched transactions
    def find_matched_unmatched(
        self, bank_transactions: List[float], system_transactions: List[float]
    ) -> Tuple[list[float], list[float], list[float]]:
        matches = []
        unmatched_bank_amounts = []
        unmatched_system_amounts = []
        bank_amounts = {}
        system_amounts = {}
        matched_amounts = set()

        for amount in bank_transactions:
            bank_amounts[amount] = bank_amounts.get(amount, 0) + 1

        for amount in system_transactions:
            system_amounts[amount] = system_amounts.get(amount, 0) + 1

        for amount in bank_amounts:
            if amount in system_amounts:
                if bank_amounts[amount] >= system_amounts[amount]:
                    for i in range(bank_amounts[amount] - system_amounts[amount]):
                        unmatched_bank_amounts.append(amount)
                    for i in range(system_amounts[amount]):
                        matches.append(amount)
                    matched_amounts.add(amount)
                elif bank_amounts[amount] < system_amounts[amount]:
                    for i in range(system_amounts[amount] - bank_amounts[amount]):
                        unmatched_system_amounts.append(amount)
                    for i in range(bank_amounts[amount]):
                        matches.append(amount)
                    matched_amounts.add(amount)
            else:
                for i in range(bank_amounts[amount]):
                    unmatched_bank_amounts.append(amount)
                matched_amounts.add(amount)

        for amount in system_amounts:
            if amount not in matched_amounts:
                for i in range(system_amounts[amount]):
                    unmatched_system_amounts.append(amount)

        print(f"matches: {matches}")
        print(f"unmatched_bank_amounts: {unmatched_bank_amounts}")
        print(f"unmatched_system_amounts: {unmatched_system_amounts}")

        return matches, unmatched_bank_amounts, unmatched_system_amounts

    def find_reconciling_matches(
        self, bank_transactions: List[float], system_transactions: List[float]
    ) -> Tuple[Dict[float, List[float]], List[float], List[float]]:
        logger = logging.getLogger(__name__)

        def find_matches_n_sum(
            nums: List, target: float, max: int, index: int, path: List, matches: List
        ) -> Any:
            copy_path = path.copy()
            if index == len(nums) or max == 0:
                if target == 0:
                    matches.append(copy_path)
            else:
                find_matches_n_sum(nums, target, max, index + 1, copy_path, matches)
                copy_path.append(nums[index])
                find_matches_n_sum(
                    nums, target - nums[index], max - 1, index + 1, copy_path, matches
                )
                copy_path.pop()

        validated_matches: Dict[float, List[float]] = {}
        matches: Dict[float, List[List[float]]] = {}

        for bank_transaction in bank_transactions:
            max_possibilties = 3 if bank_transaction <= 5000 else 5
            possible_mathces = []
            find_matches_n_sum(
                system_transactions,
                bank_transaction,
                max_possibilties,
                0,
                [],
                possible_mathces,
            )
            if possible_mathces:
                matches[bank_transaction] = possible_mathces
        while len(matches) > 0:
            unused_amounts = {}

            # Count possible amounts from system transactions to be used for reconciliation
            for amount in system_transactions:
                unused_amounts[amount] = unused_amounts.get(amount, 0) + 1

            multiple_matched_amounts = []
            for amount in matches.keys():
                # If single match found, process immediately because of better chance to be correct
                if len(matches[amount]) == 1:
                    # Check if the transaction reconcilation is possible with the current unused amounts
                    new_possible_unused_amounts = (
                        self._validate_transactions_possibility(
                            matches[amount][0], unused_amounts
                        )
                    )
                    # Update the unused amounts and remove the matched transactions
                    if new_possible_unused_amounts:
                        unused_amounts = new_possible_unused_amounts
                        system_transactions = self._remove_sub_array(
                            system_transactions, matches[amount][0]
                        )
                        bank_transactions.remove(amount)
                        validated_matches[amount] = matches[amount][0]

                # If multiple matches found, process later
                else:
                    multiple_matched_amounts.append(amount)

            # Process the multiple matched amounts
            # TODO: need to implement logic to select the best possible combination of transactions
            for amount in multiple_matched_amounts:
                for possible_match in matches[amount]:
                    new_possible_unused_amounts = (
                        self._validate_transactions_possibility(
                            possible_match, unused_amounts
                        )
                    )
                    if new_possible_unused_amounts:
                        unused_amounts = new_possible_unused_amounts
                        system_transactions = self._remove_sub_array(
                            system_transactions, possible_match
                        )
                        bank_transactions.remove(amount)
                        validated_matches[amount] = possible_match
                        break

            logger.info(f"validated_matches: {validated_matches}")
            matches = {}

            # Try to find more matches with the remaining transactions
            for bank_transaction in bank_transactions:
                max_possibilties = 3 if bank_transaction <= 5000 else 5
                possible_mathces = []
                find_matches_n_sum(
                    system_transactions,
                    bank_transaction,
                    max_possibilties,
                    0,
                    [],
                    possible_mathces,
                )
                if possible_mathces:
                    matches[bank_transaction] = possible_mathces

            logger.info(f"new matches: {matches}")

        return validated_matches, bank_transactions, system_transactions

    def _validate_transactions_possibility(
        self, amounts: List[float], possibilities: Dict[float, int]
    ) -> Dict | None:
        possibilities = possibilities.copy()
        for amount in amounts:
            if possibilities.get(amount, 0) == 0:
                return None
            else:
                possibilities[amount] -= 1
        return possibilities

    def _remove_sub_array(self, arr: List, sub_arr: List) -> List:
        for i in sub_arr:
            arr.remove(i)
        return arr
