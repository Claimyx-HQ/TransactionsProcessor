import os
import logging
from typing import List
from smtplib import SMTP
from starlette.datastructures import UploadFile
from collections import defaultdict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_error_email_with_uploadfiles(subject, body, files: List[UploadFile]):
    # Access environment variables
    logger = logging.getLogger(__name__)
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT"))  # Ensure this is an integer
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    message = MIMEMultipart()
    message['From'] = SMTP_USERNAME
    message['To'] = SMTP_USERNAME  # Adjust as necessary
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

# Initialize a dictionary to keep track of filename occurrences
    filename_counts = defaultdict(int)

    for upload_file in files:
        # Increment the count for this filename
        filename_counts[upload_file.filename] += 1
        # Determine the file's name for attachment
        if filename_counts[upload_file.filename] > 1:
            base_name, extension = os.path.splitext(upload_file.filename)
            # Format filename with count if this is not the first occurrence
            attachment_filename = f"{base_name}_{filename_counts[upload_file.filename]-1}{extension}"
        else:
            attachment_filename = upload_file.filename

        logger.info(f"Uploading to mail: {attachment_filename}")
        file_content = upload_file.file.read()
        part = MIMEApplication(file_content)
        logger.info(f"Size of {attachment_filename}: {len(file_content)} bytes")
        upload_file.file.seek(0)  # Reset file pointer after reading
        part['Content-Disposition'] = f'attachment; filename="{attachment_filename}"'
        message.attach(part)
        logger.info(f"Uploaded to mail: {attachment_filename}")

    with SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)
