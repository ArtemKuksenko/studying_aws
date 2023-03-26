from botocore import exceptions
from fastapi import APIRouter, HTTPException
from boto3_type_annotations import s3
from fastapi import UploadFile
from starlette.responses import RedirectResponse
import boto3
from botocore.client import Config

from app.settings import settings
from app.utils import get_random_string

s3_router = APIRouter(prefix='/s3', tags=[""])


def get_s3_client() -> s3.Client:
    config = {
        "config": Config(signature_version='s3v4', s3={'addressing_style': 'path'}),
        "region_name": settings.region_name,
    }
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


@s3_router.get("/upload_pictures/get_reddit_wallpaper.png", response_class=RedirectResponse)
async def get_reddit_wallpaper() -> str:
    return get_s3_image_url('reddit.wallpaper.png')


@s3_router.get("/upload_pictures/{file_name}", response_class=RedirectResponse)
async def get_upload_image(file_name: str) -> str:
    return get_s3_image_url(f"upload_pictures/{file_name}")


def get_file_name(file_name: str, s3_client: s3.Client, prefix: str = "upload_images/") -> str:
    key = f"{prefix}{get_random_string()}/{file_name}"
    try:
        s3_client.head_object(Bucket=settings.bucket_name, Key=key)
    except exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # we sure that no file by the key
            return key
        raise e
    return get_file_name(file_name, s3_client)


@s3_router.post("/upload_pictures")
def upload_file_bytes(file: UploadFile):
    mime_type, _, _ = file.content_type.partition('/')
    if mime_type != 'image':
        raise HTTPException(status_code=409, detail=f"The file is not an image.")

    s3_client = get_s3_client()
    key = get_file_name(file.filename, s3_client)

    s3_client.upload_fileobj(
        file.file,
        Bucket=settings.bucket_name,
        Key=key
    )
    return {"s3_key": key}
