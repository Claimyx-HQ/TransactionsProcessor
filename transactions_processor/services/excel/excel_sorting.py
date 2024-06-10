import logging
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

class ExcelSorting:
    def __init__(self):
        pass

    @staticmethod
    def create_table(worksheet, table_name, matches, row_index, start_col_index):
        table_range = f"{get_column_letter(start_col_index)}{row_index-1}:{get_column_letter(start_col_index+3)}{row_index-1+len(matches)}"
        table = Table(displayName=table_name, ref=table_range)
        table_style = TableStyleInfo(name="TableStyleLight9", showFirstColumn=False,
                                    showLastColumn=False, showRowStripes=False, showColumnStripes=False)
        table.tableStyleInfo = table_style
        worksheet.add_table(table)
