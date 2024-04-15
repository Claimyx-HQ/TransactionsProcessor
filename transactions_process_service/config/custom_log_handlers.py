import logging
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
import os
from transactions_process_service.services.email_sender import send_email_with_files

class EmailingTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='midnight', interval=1, backupCount=5, encoding=None, delay=False, utc=False, atTime=None, absolute_path=None):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)
        self.absolute_path = absolute_path  # Store the absolute path

    def doRollover(self):
        # Use self.absolute_path if provided, otherwise fall back to self.baseFilename
        super().doRollover()
        log_file_path = self.absolute_path if self.absolute_path else self.baseFilename
        
        yesterday = datetime.now() - timedelta(days=1)
        date_suffix = yesterday.strftime('.%Y-%m-%d')
        rotated_file_name = f"{log_file_path}{date_suffix}"

        # Perform the actual log rotation
        if os.path.exists(rotated_file_name):
            # If the file exists, proceed with sending it via email
            send_email_with_files(subject=f"Daily Log {rotated_file_name}",
                                  body="Attached is the daily log file.",
                                  files=[rotated_file_name])
        else:
            # Handle the case where the expected rotated file does not exist
            # This is a fallback mechanism and might indicate issues with the rotation logic or timing
            print(f"Expected rotated file does not exist: {rotated_file_name}")
