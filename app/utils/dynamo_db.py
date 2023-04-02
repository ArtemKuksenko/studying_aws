import boto3
from boto3_type_annotations import dynamodb

from app.settings import settings
from app.utils import config
from app.utils.task_states_const import task_states


def get_db_client() -> dynamodb.client:
    return boto3.client('dynamodb', **config)


def get_project_table() -> dynamodb.Table:
    return boto3.resource("dynamodb", **config).Table(settings.dynamo_db_table_name)


def create_task(file_path_orig: str, file_name: str, db_client: dynamodb.client = None) -> str:
    task_id = file_path_orig
    # todo be ensure, that the task_id is free
    if db_client is None:
        db_client = get_db_client()
    db_client.put_item(
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


def update_task_state(task_id: str, state: str, table: dynamodb.Table = None) -> None:
    if state not in task_states.all_states:
        raise ValueError("Not correct states")
    if table is None:
        table = get_project_table()
    table.update_item(
        Key={"task_id": task_id},
        UpdateExpression="set #state = :n",
        ExpressionAttributeNames={
            "#state": "state",
        },
        ExpressionAttributeValues={
            ":n": state,
        }
    )
