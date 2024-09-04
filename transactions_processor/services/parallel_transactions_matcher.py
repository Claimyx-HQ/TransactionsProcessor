import logging
from typing import Any, Callable, Dict, List, Tuple
import numpy as np
from transactions_processor.services.transactions_matcher import TransactionsMatcher
import multiprocessing
from multiprocessing import Pipe
from time import time


class ParallelTransactionsMatcher(TransactionsMatcher):
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

        return matches, unmatched_bank_amounts, unmatched_system_amounts

    @staticmethod
    def find_matches_n_sum(
        nums: List, target: float, max: int, index: int, path: List, matches: List
    ) -> Any:
        copy_path = path.copy()
        if index == len(nums) or max == 0:
            if target == 0:
                matches.append(copy_path)
        else:
            ParallelTransactionsMatcher.find_matches_n_sum(
                nums, target, max, index + 1, copy_path, matches
            )
            if nums[index] <= target:
                copy_path.append(nums[index])
                ParallelTransactionsMatcher.find_matches_n_sum(
                    nums,
                    round(target - nums[index], 3),
                    max - 1,
                    index + 1,
                    copy_path,
                    matches,
                )
                copy_path.pop()

    @staticmethod
    def process_chunk(
        chunk: List[float],
        system_transactions: List[float],
        conn,
        progress_dict: Dict,
        process_id: int,
        update_progress: Callable[[float], None] | None = None,
    ) -> None:
        # ) -> Dict[float, List[List[float]]]:
        matches = {}

        for i, bank_transaction in enumerate(chunk):
            progress_dict[process_id] = (i + 1) / len(chunk)
            if update_progress:
                current_progress = (
                    sum(progress_dict.values()) / len(progress_dict) * 100
                )
                update_progress(current_progress)

            max_possibilities = 3 if bank_transaction <= 5000 else 5
            possible_matches = []
            ParallelTransactionsMatcher.find_matches_n_sum(
                system_transactions,
                bank_transaction,
                max_possibilities,
                0,
                [],
                possible_matches,
            )
            if possible_matches:
                matches[bank_transaction] = possible_matches
        # return matches
        conn.send(matches)
        conn.close()

    # @staticmethod
    # def worker(chunk, system_transactions, conn):
    #     result = ParallelTransactionsMatcher.process_chunk(
    #         chunk, system_transactions, conn
    #     )
    #
    # @staticmethod
    # def worker(chunk, system_transactions, child_conn, progress_dict, process_id):
    #     start_time = time()
    #     counter = 100
    #     for i, transaction in enumerate(chunk):
    #         # process transaction
    #         if time() - start_time > 5:  # update every 5 seconds
    #             progress_dict[process_id] = (
    #                 (i + 1) / len(chunk) * 100
    #             )  # update progress in percentage
    #             start_time = time()
    #     child_conn.close()

    # @staticmethod
    # def worker(chunk, system_transactions, conn):
    #     result = ParallelTransactionsMatcher.process_chunk(
    #         chunk, system_transactions, conn
    #     )

    def find_reconciling_matches(
        self,
        bank_transactions: List[float],
        system_transactions: List[float],
        update_progress: Callable[[float], None] | None = None,
    ) -> Tuple[Dict[float, List[float]], List[float], List[float]]:
        logger = logging.getLogger(__name__)

        # Determine the number of processes to use
        num_processes = multiprocessing.cpu_count() * 2
        print(f"num_processes: {num_processes}")

        # Split bank_transactions into chunks
        chunk_size = max(1, len(bank_transactions) // num_processes)
        chunks = [
            bank_transactions[i : i + chunk_size]
            for i in range(0, len(bank_transactions), chunk_size)
        ]

        # # Create a pool of worker processes
        # with multiprocessing.Pool(processes=num_processes) as pool:
        #     # Use starmap to pass multiple arguments to the process_chunk function
        #     results = pool.starmap(
        #         ParallelTransactionsMatcher.process_chunk,
        #         [(chunk, system_transactions) for chunk in chunks],
        #     )
        processes = []
        manager = multiprocessing.Manager()
        progress_dict = manager.dict()
        pipe_list = []
        for i, chunk in enumerate(chunks):
            parent_conn, child_conn = Pipe()
            p = multiprocessing.Process(
                target=self.process_chunk,
                args=(
                    chunk,
                    system_transactions,
                    child_conn,
                    progress_dict,
                    i,
                    update_progress,
                ),
            )
            processes.append(p)
            pipe_list.append(parent_conn)
            p.start()

        # Collect results
        results = [conn.recv() for conn in pipe_list]

        # Wait for all processes to finish
        for p in processes:
            p.join()

        # Combine results from all processes
        matches = {}
        for result in results:
            matches.update(result)

        validated_matches: Dict[float, List[float]] = {}

        unused_amounts = {}

        # Count possible amounts from system transactions to be used for reconciliation
        for amount in system_transactions:
            unused_amounts[amount] = unused_amounts.get(amount, 0) + 1

        multiple_matched_amounts = []
        for amount in matches.keys():
            # If single match found, process immediately because of better chance to be correct
            if len(matches[amount]) == 1:
                # Check if the transaction reconcilation is possible with the current unused amounts
                new_possible_unused_amounts = self._validate_transactions_possibility(
                    matches[amount][0], unused_amounts
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
                new_possible_unused_amounts = self._validate_transactions_possibility(
                    possible_match, unused_amounts
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
