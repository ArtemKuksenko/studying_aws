from fastapi import APIRouter, HTTPException
from fastapi import UploadFile

from app.utils.dynamo_db import create_task, get_item
from app.utils.s3 import get_s3_image_url, get_free_file_key, get_s3_client
from app.settings import settings
from app.utils.sqs import push_sqs_message
from app.utils.task_states_const import task_states

images_router = APIRouter(prefix='/images', tags=[""])


@images_router.post("/")
def upload_file_bytes(file: UploadFile):
    mime_type, _, _ = file.content_type.partition('/')
    if mime_type != 'image':
        raise HTTPException(status_code=409, detail=f"The file is not an image.")

    s3_client = get_s3_client()
    file_key, folder = get_free_file_key(file.filename, s3_client)

    s3_client.upload_fileobj(
        file.file,
        Bucket=settings.bucket_name,
        Key=file_key
    )
    task_id = create_task(file_key, folder, file.filename)
    push_sqs_message({
        "task_id": task_id
    })
    return {
        "task_id": task_id
    }


@images_router.get("/task/{task_id}")
async def get_upload_image(task_id: str) -> dict:
    response = get_item(task_id)
    state = response['state']['S']
    if state != task_states.done:
        return {'state': state}

    return {
        'state': state,
        'image_url': get_s3_image_url(response['file_path_edited']['S'])
    }
