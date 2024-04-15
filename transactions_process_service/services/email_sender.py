import os
import logging
from typing import List, Union
from smtplib import SMTP
from starlette.datastructures import UploadFile
from collections import defaultdict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email_with_files(subject, body, files: List[Union[UploadFile|str]]):
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
        filename = upload_file if type(upload_file) is str else upload_file.filename
        logger.info(f"Processing file: {filename}")
        filename_counts[filename] += 1
        if filename_counts[filename] > 1:
            base_name, extension = os.path.splitext(filename)
            attachment_filename = f"{base_name}_{filename_counts[filename]-1}{extension}"
        else:
            attachment_filename = filename

        logger.info(f"Uploading to mail: {attachment_filename}")
        if type(upload_file) is str:
            with open(upload_file, 'rb') as f:
                file_content = f.read()
                part = MIMEApplication(file_content)
                logger.info(f"Size of {attachment_filename}: {len(file_content)} bytes")
        else:    
            file_content = upload_file.file.read()
            upload_file.file.seek(0)  # Reset file pointer after reading
            part = MIMEApplication(file_content)
            logger.info(f"Size of {attachment_filename}: {len(file_content)} bytes")
        part['Content-Disposition'] = f'attachment; filename="{attachment_filename}"'
        message.attach(part)
        logger.info(f"Uploaded to mail: {attachment_filename}")

    with SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)
