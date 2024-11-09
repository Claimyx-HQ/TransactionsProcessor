from typing import Any, List


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
            if target == 0:
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
