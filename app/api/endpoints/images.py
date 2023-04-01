from fastapi import APIRouter, HTTPException
from fastapi import UploadFile
from starlette.responses import RedirectResponse

from app.utils.dynamo_db import create_task
from app.utils.s3 import get_s3_image_url, get_free_file_key, get_s3_client
from app.settings import settings
from app.utils.sqs import push_sqs_message

images_router = APIRouter(prefix='/upload_pictures', tags=[""])


@images_router.get("/get_reddit_wallpaper.png", response_class=RedirectResponse)
async def get_reddit_wallpaper() -> str:
    return get_s3_image_url('reddit.wallpaper.png')


@images_router.get("/{file_name}", response_class=RedirectResponse)
async def get_upload_image(file_name: str) -> str:
    return get_s3_image_url(f"upload_pictures/{file_name}")


@images_router.post("/")
def upload_file_bytes(file: UploadFile):
    mime_type, _, _ = file.content_type.partition('/')
    if mime_type != 'image':
        raise HTTPException(status_code=409, detail=f"The file is not an image.")

    s3_client = get_s3_client()
    key = get_free_file_key(file.filename, s3_client)

    s3_client.upload_fileobj(
        file.file,
        Bucket=settings.bucket_name,
        Key=key
    )
    task_id = create_task(key, file.filename)
    push_sqs_message({
        "task_id": task_id
    })
    return {
        "s3_key": key,
        "task_id": task_id
    }
