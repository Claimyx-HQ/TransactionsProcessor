from typing import List, Tuple
from openpyxl.utils import get_column_letter
from transactions_processor.schemas.transaction import Transaction
from transactions_processor.services.excel.excel_sorting import ExcelSorting
from transactions_processor.services.excel.excel_utils import ExcelHelpers
from loguru import logger


class ExcelMatchesAlocator:
    @staticmethod
    def _get_full_transaction_by_amount(transaction_list, amount):
        for transaction in transaction_list:
            if transaction.amount == amount:
                transaction_list.pop(transaction_list.index(transaction))
                return transaction

    @staticmethod
    def _one_to_one_matches(
        matches: List[Tuple[Transaction, Transaction]],
        worksheet,
        system_transactions: List[Transaction],
        bank_transactions: List[Transaction],
        system_row_index: int,
        bank_row_index: int,
        system_start_col_index: int,
        bank_start_col_index: int,
        format,
    ):
        total_system_amount = 0
        total_bank_amount = 0

        logger.debug(
            f" len system: {len(system_transactions)} len bank: {len(bank_transactions)}"
        )
        if len(matches) > 0:
            system_row_index = ExcelHelpers._create_title_row(
                worksheet,
                "One to One Matches",
                column_start_index=system_start_col_index,
                row_index=system_row_index,
            )
            bank_row_index = ExcelHelpers._create_title_row(
                worksheet,
                "One to One Matches",
                column_start_index=bank_start_col_index,
                row_index=bank_row_index,
            )
            ExcelSorting.create_table(
                worksheet=worksheet,
                table_name="One_to_One_Matches_in_System_table",
                matches=matches,
                row_index=system_row_index,
                start_col_index=system_start_col_index,
            )
            ExcelSorting.create_table(
                worksheet=worksheet,
                table_name="One_to_One_Matches_in_Bank_table",
                matches=matches,
                row_index=bank_row_index,
                start_col_index=bank_start_col_index,
            )
        for value in matches:
            bank_transaction = value[0]
            system_transaction = value[1]
            ExcelHelpers._write_transaction(
                worksheet,
                system_row_index,
                system_start_col_index,
                system_transaction,
                format=format,
            )
            total_system_amount += system_transaction.amount
            ExcelHelpers._write_transaction(
                worksheet,
                bank_row_index,
                bank_start_col_index,
                bank_transaction,
                format=format,
            )
            if system_transaction in system_transactions:
                system_transactions.remove(system_transaction)
            if bank_transaction in bank_transactions:
                bank_transactions.remove(bank_transaction)
            total_bank_amount += bank_transaction.amount
            system_row_index += 1
            bank_row_index += 1

        # Add Total Row
        system_row_index = ExcelHelpers._write_total_row(
            worksheet,
            system_row_index,
            system_start_col_index,
            total_system_amount,
        )
        bank_row_index = ExcelHelpers._write_total_row(
            worksheet,
            bank_row_index,
            bank_start_col_index,
            total_bank_amount,
        )

        logger.debug("Finished writing all one to one matches")
        return system_row_index + 1, bank_row_index + 1  # Move to next row after total

    @staticmethod
    def _many_to_many_matches(
        matches: List[Tuple[List[Transaction], List[Transaction]]],
        worksheet,
        system_transactions: List[Transaction],
        bank_transactions: List[Transaction],
        system_row_index: int,
        bank_row_index: int,
        system_start_col_index: int,
        bank_start_col_index: int,
        format,
    ):
        many_to_many_color_index = 0
        total_system_amount = 0
        total_bank_amount = 0

        logger.debug(
            f" len system: {len(system_transactions)} len bank: {len(bank_transactions)}"
        )
        if len(matches) > 0:
            system_row_index = ExcelHelpers._create_title_row(
                worksheet,
                "Many to Many Matches",
                column_start_index=system_start_col_index,
                row_index=system_row_index,
            )
            bank_row_index = ExcelHelpers._create_title_row(
                worksheet,
                "Many to Many Matches",
                column_start_index=bank_start_col_index,
                row_index=bank_row_index,
            )
            count_of_bank_matches = []
            count_of_system_matches = []
            count_of_bank_matches.extend(multi_matches for match in matches for multi_matches in match[0])
            count_of_system_matches.extend(multi_matches for match in matches for multi_matches in match[1])
            ExcelSorting.create_table(
                worksheet=worksheet,
                table_name="many_to_many_Matches_in_System_table",
                matches=count_of_system_matches,
                row_index=system_row_index,
                start_col_index=system_start_col_index,
            )
            ExcelSorting.create_table(
                worksheet=worksheet,
                table_name="many_to_many_Matches_in_Bank_table",
                matches=count_of_bank_matches,
                row_index=bank_row_index,
                start_col_index=bank_start_col_index,
            )
        for match in matches:
            if many_to_many_color_index >= len(format):
                many_to_many_color_index = 0
            for bank_transaction in match[0]:
                ExcelHelpers._write_transaction(
                    worksheet,
                    bank_row_index,
                    bank_start_col_index,
                    bank_transaction,
                    format=format[many_to_many_color_index],
                )
                if bank_transaction in bank_transactions:
                    bank_transactions.remove(bank_transaction)
                total_bank_amount += bank_transaction.amount
                bank_row_index += 1
            for system_transaction in match[1]:
                ExcelHelpers._write_transaction(
                    worksheet,
                    system_row_index,
                    system_start_col_index,
                    system_transaction,
                    format=format[many_to_many_color_index],
                )
                if system_transaction in system_transactions:
                    system_transactions.remove(system_transaction)
                total_system_amount += system_transaction.amount
                system_row_index += 1
            many_to_many_color_index += 1

        # Add Total Row
        system_row_index = ExcelHelpers._write_total_row(
            worksheet,
            system_row_index,
            system_start_col_index,
            total_system_amount,
        )
        bank_row_index = ExcelHelpers._write_total_row(
            worksheet,
            bank_row_index,
            bank_start_col_index,
            total_bank_amount,
        )

        logger.debug("Finished writing all Many to Many matches")
        return system_row_index + 1, bank_row_index + 1  # Move to next row after total

    @staticmethod
    def _unmatched_system_transactions(
        unmatched_system_transactions,
        worksheet,
        system_transactions,
        system_row_index,
        system_start_col_index,
    ):
        total_system_amount = 0

        logger.debug(
            f" len system: {len(system_transactions)} and len unmatched system: {len(unmatched_system_transactions)}"
        )
        if len(unmatched_system_transactions) > 0:
            system_row_index = ExcelHelpers._create_title_row(
                worksheet,
                "Unmatched System Transactions",
                column_start_index=system_start_col_index,
                row_index=system_row_index,
            )
            ExcelSorting.create_table(
                worksheet=worksheet,
                table_name="Unmatched_System_Transactions_in_System_table",
                matches=unmatched_system_transactions,
                row_index=system_row_index,
                start_col_index=system_start_col_index,
            )

        for system_transaction in unmatched_system_transactions:
            
            ExcelHelpers._write_transaction(
                worksheet,
                system_row_index,
                system_start_col_index,
                system_transaction,
            )
            if system_transaction in system_transactions:
                system_transactions.remove(system_transaction)
            total_system_amount += system_transaction.amount
            system_row_index += 1

        # Add Total Row
        system_row_index = ExcelHelpers._write_total_row(
            worksheet,
            system_row_index,
            system_start_col_index,
            total_system_amount,
        )

        logger.debug("Finished writing all unmatched system transactions")
        return system_row_index + 1  # Move to next row after total

    @staticmethod
    def _unmatched_bank_transactions(
        unmatched_bank_transactions,
        worksheet,
        bank_transactions,
        bank_row_index,
        bank_start_col_index,
    ):
        total_bank_amount = 0

        logger.debug(
            f" len bank: {len(bank_transactions)} and len unmatched bank: {len(unmatched_bank_transactions)}"
        )
        if len(unmatched_bank_transactions) > 0:
            bank_row_index = ExcelHelpers._create_title_row(
                worksheet,
                "Unmatched Bank Transactions",
                column_start_index=bank_start_col_index,
                row_index=bank_row_index,
            )
            ExcelSorting.create_table(
                worksheet=worksheet,
                table_name="Unmatched_Bank_Transactions_in_Bank_table",
                matches=unmatched_bank_transactions,
                row_index=bank_row_index,
                start_col_index=bank_start_col_index,
            )

        for bank_transaction in unmatched_bank_transactions:
            
            ExcelHelpers._write_transaction(
                worksheet,
                bank_row_index,
                bank_start_col_index,
                bank_transaction,
            )
            if bank_transaction in bank_transactions:
                bank_transactions.remove(bank_transaction)
            total_bank_amount += bank_transaction.amount
            bank_row_index += 1

        # Add Total Row
        bank_row_index = ExcelHelpers._write_total_row(
            worksheet,
            bank_row_index,
            bank_start_col_index,
            total_bank_amount,
        )

        logger.debug("Finished writing all unmatched bank transactions")
        return bank_row_index + 1  # Move to next row after total

    @staticmethod
    def write_data(data_dict, worksheet, green_fill, color_fills: dict):
        system_row_index, bank_row_index = 3, 3
        system_start_col_index, bank_start_col_index = 1, 8
        system_transactions: List[Transaction] = data_dict["transactions"]["system"][:]
        bank_transactions: List[Transaction] = data_dict["transactions"]["bank"][:]

        logger.debug(
            f"len system: {len(system_transactions)} len bank: {len(bank_transactions)}"
        )

        logger.debug(data_dict["matches"].keys())

        for key, values in data_dict["matches"].items():
            logger.debug(f"key {key} with {len(values)} amount of values")
            if key == "one_to_one":
                system_row_index, bank_row_index = (
                    ExcelMatchesAlocator._one_to_one_matches(
                        matches=values,
                        worksheet=worksheet,
                        system_transactions=system_transactions,
                        bank_transactions=bank_transactions,
                        system_row_index=system_row_index,
                        bank_row_index=bank_row_index,
                        system_start_col_index=system_start_col_index,
                        bank_start_col_index=bank_start_col_index,
                        format=green_fill,
                    )
                )
            elif key == "many_to_many":
                system_row_index, bank_row_index = (
                    ExcelMatchesAlocator._many_to_many_matches(
                        matches=values,
                        worksheet=worksheet,
                        system_transactions=system_transactions,
                        bank_transactions=bank_transactions,
                        system_row_index=system_row_index,
                        bank_row_index=bank_row_index,
                        system_start_col_index=system_start_col_index,
                        bank_start_col_index=bank_start_col_index,
                        format=color_fills,
                    )
                )
            elif key == "unmatched_system":
                system_row_index = ExcelMatchesAlocator._unmatched_system_transactions(
                    unmatched_system_transactions=values,
                    worksheet=worksheet,
                    system_transactions=system_transactions,
                    system_row_index=system_row_index,
                    system_start_col_index=system_start_col_index,
                )
            elif key == "unmatched_bank":
                bank_row_index = ExcelMatchesAlocator._unmatched_bank_transactions(
                    unmatched_bank_transactions=values,
                    worksheet=worksheet,
                    bank_transactions=bank_transactions,
                    bank_row_index=bank_row_index,
                    bank_start_col_index=bank_start_col_index,
                )
            else:
                raise ValueError(f"Unknown key: {key}")

        logger.debug("Finished writing all transactions")
        logger.debug(
            f"Finished len system: {len(system_transactions)} len bank: {len(bank_transactions)}"
        )
        if len(system_transactions) != 0 or len(bank_transactions) != 0:
            logger.debug(f"Unmatched system transactions: {system_transactions}")
            logger.debug(f"Unmatched bank transactions: {bank_transactions}")
            raise ValueError("There are still unmatched transactions")
