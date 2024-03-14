import pandas as pd
import xlsxwriter
import io
import logging

from xlsxwriter.packager import BytesIO

from transactions_process_service.schemas.transaction import Transaction


class ExcelController:
    def create_transaction_excel(
        self,
        sorted_transactions,
        workbook_name=None,
        bank_name="Bank",
        system_name="PharmBills System",
    ) -> BytesIO | None:
        output = workbook_name
        if workbook_name is None:
            output = io.BytesIO()
        workbook, worksheet = self._create_excel(output)
        green_format, color_formats = self._setup_excel(
            workbook=workbook,
            worksheet=worksheet,
            bank_name=bank_name,
            system_name=system_name,
        )
        self._write_data(
            sorted_transactions, workbook, worksheet, green_format, color_formats
        )
        workbook.close()
        if output is not None and workbook_name is None:
            output.seek(0)
        return output

    # Private methods
    def _create_excel(self, workbook_name):
        workbook = xlsxwriter.Workbook(workbook_name)
        worksheet = workbook.add_worksheet()
        return workbook, worksheet

    def _setup_excel(
        self, workbook, worksheet, bank_name="Bank", system_name="PharmBills System"
    ):
        self._setup_headers(
            workbook=workbook,
            worksheet=worksheet,
            bank_name=bank_name,
            system_name=system_name,
        )
        green_format = workbook.add_format({"bg_color": "#C6EFCE"})
        color_formats_reversed = {
            "silver": "#C0C0C0",  # Neutral, starting with it for contrast
            "salmon": "#FA8072",
            "light_coral": "#F08080",
            "pink": "#FFC0CB",
            "fuchsia": "#FF00FF",
            "purple": "#8A2BE2",
            "medium_orchid": "#BA55D3",
            "dark_violet": "#9400D3",
            "indigo": "#4B0082",
            "navy": "#000080",
            "blue": "#0000FF",
            "dark_blue": "#00008B",
            "deep_sky_blue": "#00BFFF",
            "turquoise": "#40E0D0",
            "aqua": "#00FFFF",
            "teal": "#008080",
            "dark_green": "#006400",
            "olive": "#808000",
            "light_green": "#90EE90",
            "lime": "#00FF00",
            "yellow": "#FFFF00",  # Added for completeness
            "gold": "#FFD700",
            "orange": "#FFA500",
            "red": "#FF0000",
            "maroon": "#800000",
        }
        return green_format, color_formats_reversed

    def _setup_headers(self, workbook, worksheet, bank_name, system_name):
        merged_header_format = workbook.add_format(
            {
                "bold": True,
                "align": "center",
                "valign": "vcenter",
                "bg_color": "#DDEBF7",
            }
        )
        header_format = workbook.add_format(
            {"bold": True, "align": "center", "valign": "vcenter"}
        )
        # Setting column widths
        worksheet.set_column("A:D", 20)
        worksheet.set_column("E:E", 5)  # Empty column for separation
        worksheet.set_column("F:I", 20)
        # Merging A1:D1 and F1:I1 to create a big header
        worksheet.merge_range(
            0, 0, 0, 3, system_name, merged_header_format
        )  # Merging A1:D1 for "System Data"
        worksheet.merge_range(
            0, 5, 0, 8, bank_name, merged_header_format
        )  # Merging F1:I1 for "Bank Data"
        # Write the column headers
        headers = ["UID", "Date", "Description", "Amount"]
        for i, header in enumerate(headers):
            worksheet.write(1, i, header, header_format)  # Write System Data headers
            worksheet.write(
                1, i + 5, header, header_format
            )  # Write Bank Data headers, adjusting for the empty column
        worksheet.freeze_panes(2, 0)

    def _write_data(self, data_dict, workbook, worksheet, green_format, color_formats):
        # Example of writing data with formatting - you'll need to adapt this to your data structure
        logger = logging.getLogger(__name__)

        def _write_transaction(
            worksheet,
            row_index,
            column_start_index,
            transaction: Transaction,
            format=None,
        ):
            logger = logging.getLogger(__name__)
            logger.debug(
                f" writing transaction {transaction} in excel's row {row_index} and from column index {column_start_index}"
            )

            worksheet.write(row_index, 0 + column_start_index, transaction.uuid, format)
            worksheet.write(
                row_index,
                1 + column_start_index,
                transaction.date.strftime("%m-%d-%Y"),
                format,
            )
            worksheet.write(
                row_index, 2 + column_start_index, transaction.description, format
            )
            worksheet.write(
                row_index, 3 + column_start_index, transaction.amount, format
            )

        def _get_full_transaction_by_amount(transaction_list, amount):
            for transaction in transaction_list:
                if transaction["amount"] == amount:
                    transaction_list.pop(transaction_list.index(transaction))
                    return transaction

        system_row_index, bank_row_index = 3, 3
        multi_to_one_color_index = 0
        system_start_col_index, bank_start_col_index = 0, 5
        system_transactions = data_dict["transactions"]["system"]
        bank_transactions = data_dict["transactions"]["bank"]

        logger.debug(
            f"len system: {len(system_transactions)} len bank: {len(bank_transactions)}"
        )

        color_formats = {
            index: workbook.add_format({"bg_color": value})
            for index, (key, value) in enumerate(color_formats.items())
        }

        for key, values in data_dict["matches"].items():
            logger.debug(f"key {key} with {len(values)} amount of values")
            if key == "one_to_one":
                logger.debug(
                    f" len system: {len(system_transactions)} len bank: {len(bank_transactions)}"
                )
                for value in values:
                    _write_transaction(
                        worksheet,
                        system_row_index,
                        system_start_col_index,
                        _get_full_transaction_by_amount(system_transactions, value),
                        format=green_format,
                    )
                    _write_transaction(
                        worksheet,
                        bank_row_index,
                        bank_start_col_index,
                        _get_full_transaction_by_amount(bank_transactions, value),
                        format=green_format,
                    )
                    system_row_index += 1
                    bank_row_index += 1
                logger.debug("Finished writing all one to one matches")
            elif key == "multi_to_one":
                logger.debug(
                    f" len system: {len(system_transactions)} len bank: {len(bank_transactions)}"
                )
                for bank_transaction, system_combination_transactions in values.items():
                    if multi_to_one_color_index >= len(color_formats):
                        multi_to_one_color_index = 0
                    _write_transaction(
                        worksheet,
                        bank_row_index,
                        bank_start_col_index,
                        _get_full_transaction_by_amount(
                            bank_transactions, amount=bank_transaction
                        ),
                        format=color_formats[multi_to_one_color_index],
                    )
                    bank_row_index += 1
                    for transaction in system_combination_transactions:
                        _write_transaction(
                            worksheet,
                            system_row_index,
                            system_start_col_index,
                            _get_full_transaction_by_amount(
                                system_transactions, amount=transaction
                            ),
                            color_formats[multi_to_one_color_index],
                        )
                        system_row_index += 1
                    multi_to_one_color_index += 1
                logger.debug("Finished writing all multi to one matches")
            elif key == "unmatched_system":
                logger.debug(
                    f" len system: {len(system_transactions)} len bank: {len(bank_transactions)}"
                )
                for value in values:
                    _write_transaction(
                        worksheet,
                        system_row_index,
                        system_start_col_index,
                        _get_full_transaction_by_amount(system_transactions, value),
                    )
                    system_row_index += 1
                logger.debug("Finished writing all unmatched system transactions")
            elif key == "unmatched_bank":
                logger.debug(
                    f" len system: {len(system_transactions)} len bank: {len(bank_transactions)}"
                )
                for value in values:
                    _write_transaction(
                        worksheet,
                        bank_row_index,
                        bank_start_col_index,
                        _get_full_transaction_by_amount(bank_transactions, value),
                    )
                    bank_row_index += 1
                logger.debug("Finished writing all unmatched bank transactions")
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
