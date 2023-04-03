import json

from app.controller.images import rotate_image
from app.settings import settings
from app.controller.dynamo_db import update_task_state, get_project_table
from app.controller.s3 import download_file, get_s3_client
from app.controller.sqs import pull_one_message
from app.controller.task_states_const import task_states


def process_the_task_image(task: dict[str, str]) -> str:
    s3_client = get_s3_client()

    file = download_file(task['file_path_orig'], s3_client=s3_client)
    processed_file = rotate_image(file)

    file_key = task['file_path_orig'].replace(
        settings.upload_images_folder,
        settings.download_images_folder
    )
    file_key = f"{file_key}.gif"

    s3_client.upload_fileobj(
        processed_file,
        Bucket=settings.bucket_name,
        Key=file_key
    )
    return file_key


def main(*args) -> dict:
    if args:
        print("event = {}".format(args[0]))
    print(f"args: {args}")
    message = pull_one_message()
    print("message is uploaded")
    task_id = json.loads(message.body)["task_id"]
    print(f"task_id: {task_id}")
    table = get_project_table()
    task = update_task_state(task_id, task_states.in_progress, table=table, return_values='ALL_NEW')

    try:
        print("start task processing")
        file_path_edited = process_the_task_image(task)
        print("task is processed")

        table.update_item(
            Key={"task_id": task_id},
            UpdateExpression="set #file_path_edited = :p, #state = :s",
            ExpressionAttributeNames={
                "#file_path_edited": "file_path_edited",
                "#state": "state",
            },
            ExpressionAttributeValues={
                ":p": file_path_edited,
                ":s": task_states.done,
            }
        )
    except Exception as e:
        print(e)
        update_task_state(task_id, task_states.crashed, table=table)
        res_task = task_states.crashed
        file_path_edited = None
    else:
        res_task = task_states.done

    dropped = message.delete()
    return {
        "status": 200,
        "task_id": task_id,
        "task": res_task,
        "file_path_edited": file_path_edited,
        "dropped": bool(dropped)
    }


if __name__ == "__main__":
    main()
