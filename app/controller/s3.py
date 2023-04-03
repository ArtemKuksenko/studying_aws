from typing import Tuple

import boto3
from fastapi import HTTPException

from app.controller import config
from app.settings import settings
from boto3_type_annotations import s3
from botocore import exceptions

from app.utils import get_random_string


def get_s3_client() -> s3.Client:
    return boto3.client('s3', **config)


def get_s3_image_url(key: str, s3_client: s3.Client = None) -> str:
    """
    Get temporary URL of image by s3 key
    """
    if s3_client is None:
        s3_client = get_s3_client()

    try:
        s3_client.head_object(Bucket=settings.bucket_name, Key=key)
    except exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            raise HTTPException(status_code=404, detail=f"Image not found")
        raise e

    return s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.bucket_name,
            'Key': key,
        },
        ExpiresIn=3600,
    )


def download_file(key: str, s3_client: s3.Client = None) -> bytes:
    if s3_client is None:
        s3_client = get_s3_client()
    s3_response_object = s3_client.get_object(Bucket=settings.bucket_name, Key=key)
    object_content = s3_response_object['Body'].read()
    return object_content


def get_free_file_key(file_name: str, s3_client: s3.Client) -> Tuple[str, str]:
    folder_name = get_random_string()
    key = f"{settings.upload_images_folder}/{folder_name}/{file_name}"
    try:
        s3_client.head_object(Bucket=settings.bucket_name, Key=key)
    except exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # we sure that no file by the key
            return key, folder_name
        raise e
    return get_free_file_key(file_name, s3_client)
