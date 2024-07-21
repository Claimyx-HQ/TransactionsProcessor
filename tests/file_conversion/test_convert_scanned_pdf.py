from transactions_processor.services.converters.scanned_pdf_converter import (
    ScannedPDFConverter,
)


def test_convert_scanned_pdf():
    pdf_converter = ScannedPDFConverter()
    file_key = "flagstar_bank_scanned.pdf"
    converted_file = pdf_converter.get_converted_pdf(file_key)
    assert converted_file is not None
