import ocrmypdf
from transactions_processor.services.converters.scanned_pdf_converter import (
    ScannedPDFConverter,
)


def test_convert_scanned_pdf():
    pdf_converter = ScannedPDFConverter()
    input_file = "tests/data/etc/flagstar_bank_scanned.pdf"
    converted_pdf = pdf_converter.convert_scanned_pdf(input_file)
    with open("tests/output_tests_data/flagstar_bank_converted.pdf", "wb") as f:
        f.write(converted_pdf.read())
    assert True
