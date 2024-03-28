import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from smtplib import SMTP
from fastapi import UploadFile
from typing import List


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

    for upload_file in files:
        logger.info(f"Uploading to mail : {upload_file.filename}")
        file_content = upload_file.file.read()
        part = MIMEApplication(file_content)
        logger.info(f"Size of {upload_file.filename}: {len(file_content)} bytes")
        upload_file.file.seek(0)  # Reset file pointer after reading
        part['Content-Disposition'] = f'attachment; filename="{upload_file.filename}"'
        message.attach(part)
        logger.info(f"Uploaded to mail : {upload_file.filename}")

    with SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)
