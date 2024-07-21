import requests
import io

from transactions_processor.utils.aws_utils import retrieve_file


class ScannedPDFConverter:
    def __init__(self):
        pass

    def get_converted_pdf(self, file_key: str) -> io.BytesIO | None:
        function_url = (
            "https://r24ceitrkfv6r4gkql23g3unwi0qurog.lambda-url.us-east-2.on.aws"
        )

        # Data to send (if any)
        data = {"file_key": file_key}

        # Send a POST request to the function URL
        response = requests.post(function_url, json=data)

        # Check the response
        if response.status_code == 200:
            pdf_key = response.json()["file_key"]
            converted_file = retrieve_file("bankrectool-files", pdf_key)
            return converted_file
        else:
            print("Request failed with status code:", response.status_code)
            print("Response:", response.text)
