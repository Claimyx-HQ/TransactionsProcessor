import csv
from typing import BinaryIO
import xlrd
from openpyxl import load_workbook


def get_csv_first_cell(file_path) -> str:
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        first_row = next(reader)
        if first_row:
            return first_row[0]
        raise ValueError("Empty CSV file")


def get_xls_first_cell(file: BinaryIO):
    file_contents = file.read()
    workbook = xlrd.open_workbook(file_contents=file_contents)
    sheet = workbook.sheet_by_index(0)
    file.seek(0)
    return sheet.cell_value(0, 0)


def get_xlsx_first_cell(file_path):
    wb = load_workbook(filename=file_path, read_only=True)
    sheet = wb.active
    assert sheet is not None
    return sheet["A1"].value
