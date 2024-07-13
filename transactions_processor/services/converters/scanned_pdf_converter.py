import ocrmypdf
import io


class ScannedPDFConverter:
    def __init__(self):
        pass

    def convert_scanned_pdf(self, input_file) -> io.BytesIO:
        output_file = io.BytesIO()
        ocrmypdf.ocr(
            input_file, output_file, deskew=True, use_threads=True, progress_bar=False
        )
        output_file.seek(0)
        return output_file
