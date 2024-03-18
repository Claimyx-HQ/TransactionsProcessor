import logging
from openpyxl.utils import get_column_letter
from transactions_process_service.schemas.transaction import Transaction
from transactions_process_service.services.excel_creation.excel_helper_functions import (
    ExcelHelpers,
)
from transactions_process_service.services.excel_creation.excel_sorting import (
    ExcelSorting,
)


class ExcelMatchesAlocator:
    @staticmethod
    def _get_full_transaction_by_amount(transaction_list, amount):
        for transaction in transaction_list:
            if transaction["amount"] == amount:
                transaction_list.pop(transaction_list.index(transaction))
                return transaction

    @staticmethod
    def _one_to_one_matches(
        matches,
        worksheet,
        system_transactions,
        bank_transactions,
        system_row_index,
        bank_row_index,
        system_start_col_index,
        bank_start_col_index,
        format,
    ) -> None:
        logger = logging.getLogger(__name__)
        logger.debug(
            f" len system: {len(system_transactions)} len bank: {len(bank_transactions)}"
        )
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
            ExcelHelpers._write_transaction(
                worksheet,
                system_row_index,
                system_start_col_index,
                ExcelMatchesAlocator._get_full_transaction_by_amount(
                    system_transactions, value
                ),
                format=format,
            )
            ExcelHelpers._write_transaction(
                worksheet,
                bank_row_index,
                bank_start_col_index,
                ExcelMatchesAlocator._get_full_transaction_by_amount(
                    bank_transactions, value
                ),
                format=format,
            )
            system_row_index += 1
            bank_row_index += 1

        logger.debug("Finished writing all one to one matches")
        return system_row_index, bank_row_index

    @staticmethod
    def _multi_to_one_matches(
        matches,
        worksheet,
        system_transactions,
        bank_transactions,
        system_row_index,
        bank_row_index,
        system_start_col_index,
        bank_start_col_index,
        format,
    ) -> None:
        logger = logging.getLogger(__name__)
        multi_to_one_color_index = 0
        logger.debug(
            f" len system: {len(system_transactions)} len bank: {len(bank_transactions)}"
        )
        system_row_index = ExcelHelpers._create_title_row(
            worksheet,
            "Multi to One Matches",
            column_start_index=system_start_col_index,
            row_index=system_row_index,
        )
        bank_row_index = ExcelHelpers._create_title_row(
            worksheet,
            "Multi to One Matches",
            column_start_index=bank_start_col_index,
            row_index=bank_row_index,
        )
        multi_matches = [system_transaction for key, values in matches.items() for system_transaction in values]
        ExcelSorting.create_table(
            worksheet=worksheet,
            table_name="Multi_to_One_Matches_in_System_table",
            matches=multi_matches,
            row_index=system_row_index,
            start_col_index=system_start_col_index,
        )
        ExcelSorting.create_table(
            worksheet=worksheet,
            table_name="Multi_to_One_Matches_in_Bank_table",
            matches=matches,
            row_index=bank_row_index,
            start_col_index=bank_start_col_index,
        )
        for bank_transaction, system_combination_transactions in matches.items():
            if multi_to_one_color_index >= len(format):
                multi_to_one_color_index = 0
            ExcelHelpers._write_transaction(
                worksheet,
                bank_row_index,
                bank_start_col_index,
                ExcelMatchesAlocator._get_full_transaction_by_amount(
                    bank_transactions, amount=bank_transaction
                ),
                format=format[multi_to_one_color_index],
            )
            bank_row_index += 1
            for transaction in system_combination_transactions:
                ExcelHelpers._write_transaction(
                    worksheet,
                    system_row_index,
                    system_start_col_index,
                    ExcelMatchesAlocator._get_full_transaction_by_amount(
                        system_transactions, amount=transaction
                    ),
                    format=format[multi_to_one_color_index],
                )
                system_row_index += 1
            multi_to_one_color_index += 1
        logger.debug("Finished writing all multi to one matches")
        return system_row_index, bank_row_index

    @staticmethod
    def _unmatched_system_transactions(
        unmatched_system_transactions,
        worksheet,
        system_transactions,
        system_row_index,
        system_start_col_index,
    ) -> None:
        logger = logging.getLogger(__name__)
        logger.debug(
            f" len system: {len(system_transactions)} and len unmatched system: {len(unmatched_system_transactions)}"
        )
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
        

        for value in unmatched_system_transactions:
            ExcelHelpers._write_transaction(
                worksheet,
                system_row_index,
                system_start_col_index,
                ExcelMatchesAlocator._get_full_transaction_by_amount(
                    system_transactions, value
                ),
            )
            system_row_index += 1
        logger.debug("Finished writing all unmatched system transactions")
        return system_row_index

    @staticmethod
    def _unmatched_bank_transactions(
        unmatched_bank_transactions,
        worksheet,
        bank_transactions,
        bank_row_index,
        bank_start_col_index,
    ) -> None:
        logger = logging.getLogger(__name__)
        logger.debug(
            f" len bank: {len(bank_transactions)} and len unmatched bank: {len(unmatched_bank_transactions)}"
        )
        bank_row_index = ExcelHelpers._create_title_row(
            worksheet,
            "Unmatched Bank Transactions",
            column_start_index=bank_start_col_index,
            row_index=bank_row_index,
        )
        ExcelSorting.create_table(
            worksheet=worksheet,
            table_name="Unmatched_Bank_Transactions_in_System_table",
            matches=unmatched_bank_transactions,
            row_index=bank_row_index,
            start_col_index=bank_start_col_index,
        )

        for value in unmatched_bank_transactions:
            ExcelHelpers._write_transaction(
                worksheet,
                bank_row_index,
                bank_start_col_index,
                ExcelMatchesAlocator._get_full_transaction_by_amount(
                    bank_transactions, value
                ),
            )
            bank_row_index += 1
        logger.debug("Finished writing all unmatched bank transactions")
        return bank_row_index

    @staticmethod
    def write_data(data_dict, worksheet, green_fill, color_fills: dict):
        logger = logging.getLogger(__name__)
        system_row_index, bank_row_index = 3, 3
        system_start_col_index, bank_start_col_index = 1, 6
        system_transactions = data_dict["transactions"]["system"]
        bank_transactions = data_dict["transactions"]["bank"]

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

            elif key == "multi_to_one":
                system_row_index, bank_row_index = (
                    ExcelMatchesAlocator._multi_to_one_matches(
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
        if len(system_transactions) != 0 and len(bank_transactions) != 0:
            logger.debug(f"system_transactions: {system_transactions}")
            logger.debug(f"bank_transactions: {bank_transactions}")
            raise ValueError("There are still unmatched transactions")
