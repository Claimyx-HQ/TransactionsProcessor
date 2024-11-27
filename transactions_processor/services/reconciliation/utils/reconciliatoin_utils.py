from typing import Any, Dict, List, Tuple

from transactions_processor.schemas.transaction import Transaction


class ReconciliationUtils:

    @staticmethod
    def find_matches_n_sum(
        nums: List[float],
        target: float,
        max: int,
        index: int,
        path: List[float],
        matches: List[List[float]],
    ) -> Any:
        copy_path = path.copy()
        if index == len(nums) or max == 0:
            if target == 0 and len(copy_path) > 0:
                matches.append(copy_path)
        else:
            ReconciliationUtils.find_matches_n_sum(
                nums, target, max, index + 1, copy_path, matches
            )
            if nums[index] <= target:
                copy_path.append(nums[index])
                ReconciliationUtils.find_matches_n_sum(
                    nums,
                    round(target - nums[index], 3),
                    max - 1,
                    index + 1,
                    copy_path,
                    matches,
                )
                copy_path.pop()

    @staticmethod
    def group_by_description(
        transactions: List[Transaction],
    ) -> List[List[Transaction]]:
        grouped_transactions: Dict[str, List[Transaction]] = {}
        for transaction in transactions:
            key = transaction.description[:3]
            grouped_transactions[key] = grouped_transactions.get(key, [])
            grouped_transactions[key].append(transaction)

        # remove single transactions
        grouped_transactions = {
            k: v for k, v in grouped_transactions.items() if len(v) > 1
        }

        return list(grouped_transactions.values())
