import boto3
from boto3_type_annotations import dynamodb

from app.settings import settings
from app.utils import config
from app.utils.task_states_const import task_states


def get_db_client() -> dynamodb.client:
    return boto3.client('dynamodb', **config)


def create_task(file_path_orig: str, file_name: str) -> str:
    task_id = file_path_orig
    # todo be ensure, that the task_id is free
    get_db_client().put_item(
        TableName=settings.dynamo_db_table_name,
        Item={
            "task_id": {
                "S": task_id
            },
            "file_name": {
                "S": file_name
            },
            "file_path_orig": {
                "S": file_path_orig
            },
            "file_path_edited": {
                "S": ""
            },
            "state": {
                "S": task_states.created
            }
        }
    )
    return task_id
