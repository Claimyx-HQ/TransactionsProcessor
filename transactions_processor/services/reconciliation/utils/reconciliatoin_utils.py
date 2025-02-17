from collections import defaultdict
from typing import Any, Dict, List, Tuple
from numba import njit
from numba.typed import List as NumbaList
import numpy as np
from numba import types

from transactions_processor.schemas.transaction import Transaction


@njit
def numba_find_combinations(
    system_scaled,  # 1D np.ndarray of int64
    system_orig,  # 1D np.ndarray of float64
    results,  # typed List of 1D np.ndarray (float64) [output]
    max_depth,  # int: maximum combination length
    scaled_target,  # int: target sum scaled up
    scaled_tolerance,  # int: allowed tolerance (scaled)
):

    def clone_list(lst):
        new_lst = NumbaList.empty_list(types.int64)
        for i in range(len(lst)):
            new_lst.append(lst[i])
        return new_lst

    # The stack holds tuples of (current index, current sum, current depth, current combination)
    stack = NumbaList()
    empty_combo = NumbaList.empty_list(types.int64)
    stack.append((0, 0, 0, empty_combo))

    while len(stack) > 0:
        idx, current_sum, depth, combo = stack.pop()

        # If a nonempty combination sums to within tolerance, record it.
        if abs(current_sum - scaled_target) <= scaled_tolerance and len(combo) > 0:
            arr = np.empty(len(combo), dtype=np.float64)
            for i in range(len(combo)):
                # Use the indices in combo to retrieve original values
                arr[i] = system_orig[combo[i]]
            results.append(arr)

        # Stop expanding this branch if we've reached max depth or the end of the list.
        if depth >= max_depth or idx >= len(system_scaled):
            continue

        current_value = system_scaled[idx]

        # Prune branches that would exceed the target.
        if current_sum + current_value > scaled_target + scaled_tolerance:
            continue

        # (Optional) Skip duplicates if desired. Here we simply rely on sorted order.
        # if idx > 0 and system_scaled[idx] == system_scaled[idx - 1]:
        #    continue

        # Branch 1: Include the current element.
        new_combo = clone_list(combo)
        new_combo.append(idx)
        stack.append((idx + 1, current_sum + current_value, depth + 1, new_combo))

        # Branch 2: Exclude the current element.
        stack.append((idx + 1, current_sum, depth, clone_list(combo)))
    return results


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
    def find_matches_n_sum2(
        nums: List[float], target: float, max_elements: int, tolerance: float = 1e-6
    ) -> List[List[float]]:
        scaled_nums = [int(round(x * 10000)) for x in nums]
        scaled_target = int(round(target * 10000))
        scaled_tolerance = int(round(tolerance * 10000))

        nums_sorted = sorted(zip(scaled_nums, nums), key=lambda x: x[0])
        results = []

        def backtrack(start, path, current_sum, remaining_depth):
            if abs(current_sum - scaled_target) <= scaled_tolerance:
                results.append([x[1] for x in path])
                return
            if remaining_depth == 0 or start >= len(nums_sorted):
                return

            for i in range(start, len(nums_sorted)):
                num_scaled, num_orig = nums_sorted[i]
                # Early termination for sorted list
                if current_sum + num_scaled > scaled_target + scaled_tolerance:
                    break
                # Skip duplicates
                if i > start and nums_sorted[i] == nums_sorted[i - 1]:
                    continue

                path.append((num_scaled, num_orig))
                backtrack(i + 1, path, current_sum + num_scaled, remaining_depth - 1)
                path.pop()

        backtrack(0, [], 0, max_elements)
        return results

    @staticmethod
    def find_matches_n_sum3(
        nums: List[float], target: float, max_elements: int, tolerance: float = 1e-6
    ) -> List[List[float]]:
        # Convert to integers (millicents for 4 decimal places precision)
        scaled_nums = [int(round(x * 10000)) for x in nums]
        scaled_target = int(round(target * 10000))
        scaled_tolerance = int(round(tolerance * 10000))

        # Sort with original values and compute prefix sums
        sorted_pairs = sorted(zip(scaled_nums, nums), key=lambda x: x[0])
        scaled_sorted, orig_sorted = zip(*sorted_pairs) if sorted_pairs else ([], [])
        n = len(scaled_sorted)

        # Precompute prefix sums for pruning
        prefix_sum = [0] * (n + 1)
        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + scaled_sorted[i]

        results = []

        def backtrack(start: int, path: List[float], current_sum: int, depth_left: int):
            # Match found condition
            if abs(current_sum - scaled_target) <= scaled_tolerance:
                results.append([x[1] for x in path])
                return

            # Early termination conditions
            if depth_left == 0 or start >= n:
                return

            # Available elements and pruning calculations
            available = n - start
            if available < depth_left:
                return

            # Calculate min/max possible sums for current path
            min_possible = prefix_sum[start + depth_left] - prefix_sum[start]
            max_possible = (
                prefix_sum[start + available]
                - prefix_sum[start + available - depth_left]
            )

            if current_sum + min_possible > scaled_target + scaled_tolerance:
                return
            if current_sum + max_possible < scaled_target - scaled_tolerance:
                return

            # Main backtracking loop
            for i in range(start, n):
                num = scaled_sorted[i]
                orig = orig_sorted[i]

                # Early exit for sorted list
                if current_sum + num > scaled_target + scaled_tolerance:
                    break

                # Skip duplicates
                if i > start and scaled_sorted[i] == scaled_sorted[i - 1]:
                    continue

                backtrack(
                    i + 1, path + [(num, orig)], current_sum + num, depth_left - 1
                )

        backtrack(0, [], 0, max_elements)
        return results

    def find_matches_optimized(
        system_amounts, bank_amount, max_elements, tolerance: float = 1e-6
    ):
        # Ensure input is a NumPy array.
        system_np = np.array(system_amounts, dtype=np.float64)
        scale_factor = 10000
        scaled_system = np.round(system_np * scale_factor).astype(np.int64)
        scaled_target = int(round(bank_amount * scale_factor))
        scaled_tolerance = int(round(tolerance * scale_factor))

        # Sort the values (and their corresponding originals) so that we can apply early termination.
        sort_idx = np.argsort(scaled_system)
        system_scaled_sorted = scaled_system[sort_idx]
        system_orig_sorted = system_np[sort_idx]

        # Initialize a typed list for results.
        results = NumbaList.empty_list(types.Array(types.float64, 1, "C"))

        # Call the Numba-accelerated backtracking function.
        numba_find_combinations(
            system_scaled_sorted,
            system_orig_sorted,
            results,
            max_elements,
            scaled_target,
            scaled_tolerance,
        )

        # Convert NumPy arrays back to Python lists.
        return [arr.tolist() for arr in results]

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
