import os
import openpyxl
import io
import logging
from typing import Union

from transactions_processor.services.excel.excel_matches_functions import ExcelMatchesAlocator
from transactions_processor.services.excel.excel_utils import ExcelHelpers


class ExcelController:
    def create_transaction_excel(
        self,
        sorted_transactions,
        workbook_name: Union[str, None] = None,
        bank_name="Bank",
        system_name="PharmBills System",
    ) -> io.BytesIO | None:
        output = io.BytesIO() if workbook_name is None else workbook_name
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        green_fill, color_fills = ExcelHelpers._setup_excel(
            worksheet=worksheet,
            bank_name=bank_name,
            system_name=system_name,
        )
        ExcelMatchesAlocator.write_data(
            sorted_transactions, worksheet, green_fill, color_fills
        )
        if workbook_name is None:
            workbook.save(output)
            output.seek(0)
        else:
            folder_path = os.path.dirname(workbook_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            workbook.save(workbook_name)
        return output

    # Private methods
