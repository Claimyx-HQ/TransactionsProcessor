from typing import Any, BinaryIO
import boto3

def upload_file_to_s3(s3_client: Any,file: BinaryIO, bucket: str, key: str):
    s3_client.upload_fileobj(file, bucket, key)
    presigned_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=3600
    )
    return presigned_url
