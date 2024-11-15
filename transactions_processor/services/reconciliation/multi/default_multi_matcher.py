from loguru import logger
from typing import Any, Callable, Dict, List, Match, Tuple
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.schemas.transactions_matcher import ReconcilingMatches
from transactions_processor.services.reconciliation.multi.multi_matcher import (
    MultiMatcher,
)
import multiprocessing
from multiprocessing import Pipe

from transactions_processor.services.reconciliation.utils.progress_callback import (
    ProgressCallback,
)
from transactions_processor.services.reconciliation.utils.reconciliatoin_utils import (
    ReconciliationUtils,
)
from transactions_processor.services.reconciliation.utils.transaction_utils import (
    TransactionUtils,
)


class DefaultMultiMatcher(MultiMatcher):
    # Return matching and unmatched transactions
    def __init__(self, update_progress: ProgressCallback | None = None):
        self.update_progress = update_progress

    def set_update_progress(self, update_progress: ProgressCallback) -> None:
        self.update_progress = update_progress

    @staticmethod
    def process_chunk(
        chunk: List[float],
        system_transactions_groups: List[List[float]],
        max_matches: int,
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

            # max_possibilities = 3 if bank_transaction <= 5000 else max_matches
            max_possibilities = max_matches
            possible_matches = []
            for system_transactions in system_transactions_groups:
                ReconciliationUtils.find_matches_n_sum(
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

    def reoncile_transactions(
        self,
        bank_transactions: List[Transaction],
        system_transactions_groups: List[List[Transaction]],
        max_matches: int,
        system_transactions: List[Transaction],
    ):
        bank_amounts = [transaction.amount for transaction in bank_transactions]
        # system_amounts = [transaction.amount for transaction in system_transactions]
        system_amounts = []
        system_amounts_groups = []
        for group in system_transactions_groups:
            system_amounts.extend([transaction.amount for transaction in group])
            system_amounts_groups.append([transaction.amount for transaction in group])

        matches = self._run_reconciliation_processes(
            bank_amounts, system_amounts_groups, max_matches, self.update_progress
        )

        validated_matches: Dict[float, List[float]] = {}

        unused_amounts = {}

        # Count possible amounts from system transactions to be used for reconciliation
        for amount in system_amounts:
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
                    system_amounts = self._remove_sub_array(
                        system_amounts, matches[amount][0]
                    )
                    bank_amounts.remove(amount)
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
                    system_amounts = self._remove_sub_array(
                        system_amounts, possible_match
                    )
                    bank_amounts.remove(amount)
                    validated_matches[amount] = possible_match
                    break

        logger.info(f"validated_matches: {validated_matches}")

        return validated_matches, bank_amounts, system_amounts

    def find_one_to_many(
        self,
        bank_transactions: List[Transaction],
        system_transactions: List[Transaction],
        max_matches: int,
    ) -> ReconcilingMatches:
        grouped_transactions = ReconciliationUtils.group_by_description(
            system_transactions
        )
        validated_matches, unmatched_bank_amounts, unmatched_system_amounts = (
            self.reoncile_transactions(
                bank_transactions,
                grouped_transactions,
                max_matches,
                system_transactions,
            )
        )

        matches = TransactionUtils.matched_amounts_to_transactions(
            validated_matches, {}, bank_transactions, system_transactions
        )
        return matches

    def _run_reconciliation_processes(
        self,
        bank_amounts: List[float],
        system_amounts_groups: List[List[float]],
        max_matches: int,
        update_progress: Callable[[float], None] | None = None,
    ) -> Dict[float, List[List[float]]]:
        num_processes = multiprocessing.cpu_count() * 2
        print(f"num_processes: {num_processes}")

        chunk_size = max(1, len(bank_amounts) // num_processes)
        chunks = [
            bank_amounts[i : i + chunk_size]
            for i in range(0, len(bank_amounts), chunk_size)
        ]

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
                    system_amounts_groups,
                    max_matches,
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

        matches = {}
        for result in results:
            matches.update(result)

        return matches

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
