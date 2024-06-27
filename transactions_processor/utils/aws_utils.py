from typing import Any, BinaryIO
import requests
import boto3
import hashlib


def upload_file_to_s3(s3_client: Any, file: BinaryIO, bucket: str, key: str):
    s3_client.upload_fileobj(file, bucket, key)
    presigned_url = s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600
    )
    return presigned_url


def notify_client(client_id, message, timeout=5):
    try:
        response = requests.post(
            "https://api.bankrectool.com/notify",
            json={"clientId": client_id, "message": message},
            timeout=timeout,
        )
        if response.status_code == 200:
            print(f"Successfully notified client {client_id}, message: {message}")
        else:
            print(f"Failed to notify client {client_id}: {response.text}")
    except Exception as e:
        print(f"Failed to notify client {client_id}: {e}")


def generate_error_code(error: Exception) -> str:
    error_message = str(error)
    error_string = f"{error_message}"
    hash_object = hashlib.md5(error_string.encode())
    error_code = hash_object.hexdigest()[:8]  # Use first 8 characters of the hash

    return error_code
