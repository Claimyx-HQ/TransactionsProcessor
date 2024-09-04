from typing import Any, BinaryIO
import requests
import boto3
from botocore.config import Config
import hashlib
import io
from loguru import logger


s3_client = boto3.client("s3", config=Config(signature_version="s3v4"))


def upload_file_to_s3(file: BinaryIO, bucket: str, key: str):
    s3_client.upload_fileobj(file, bucket, key)
    presigned_url = s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600
    )
    return presigned_url


def retrieve_file(bucket_name, key) -> BinaryIO:
    file_obj = s3_client.get_object(Bucket=bucket_name, Key=key)
    file_content = file_obj["Body"].read()
    file = io.BytesIO(file_content)
    return file


def notify_client(client_id, message, timeout=5):
    try:
        response = requests.post(
            "https://api.bankrectool.com/notify",
            json={"clientId": client_id, "message": message},
            timeout=timeout,
        )
        if response.status_code == 200:
            logger.info(f"Successfully notified client {client_id}, message: {message}")
        else:
            logger.error(f"Failed to notify client {client_id}: {response.text}")
    except Exception as e:
        logger.error(f"Failed to notify client {client_id}: {e}")


def generate_error_code(error: Exception) -> str:
    error_message = str(error)
    error_string = f"{error_message}"
    hash_object = hashlib.md5(error_string.encode())
    error_code = hash_object.hexdigest()[:8]  # Use first 8 characters of the hash

    return error_code
