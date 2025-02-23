import csv
from typing import BinaryIO
import xlrd
from openpyxl import load_workbook
import pandas as pd
import chardet
import io


def get_csv_first_cell(file: BinaryIO) -> str:
    # Read a small sample to detect encoding if possible
    sample_bytes = file.read(1024)
    file.seek(0)  # Reset pointer to the beginning for further reading

    if chardet:
        detection = chardet.detect(sample_bytes)
        encoding = detection.get("encoding", "utf-8")
    else:
        encoding = "utf-8"

    buffer = io.BytesIO(sample_bytes)
    csv_reader = csv.reader(buffer.read().decode(encoding).splitlines())

    try:
        first_row = next(csv_reader)
    except StopIteration:
        raise ValueError("The CSV file is empty.")

    if not first_row:
        raise ValueError("The first row in the CSV file is empty.")

    return first_row[0]


def get_xls_first_cell(file: BinaryIO):
    file.seek(0)
    file_contents = file.read()
    workbook = xlrd.open_workbook(file_contents=file_contents)
    sheet = workbook.sheet_by_index(0)
    file.seek(0)
    return sheet.cell_value(0, 0)


def get_xlsx_first_cell(file: BinaryIO):
    wb = load_workbook(filename=file, read_only=True)
    sheet = wb.active
    assert sheet is not None
    return sheet["A1"].value
