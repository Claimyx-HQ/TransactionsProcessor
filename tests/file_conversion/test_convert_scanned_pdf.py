from transactions_processor.services.converters.scanned_pdf_converter import (
    ScannedPDFConverter,
)


def test_convert_scanned_pdf():
    pdf_converter = ScannedPDFConverter()
    file_key = "tomball_baylor.pdf"
    converted_file = pdf_converter.get_converted_pdf(file_key)

    if converted_file is not None:
        with open("tests/output_tests_data/tomball_baylor_converted.pdf", "wb") as f:
            f.write(converted_file.getvalue())

    assert converted_file is not None
