import json

from app.controller.images import process_image
from app.utils.dynamo_db import update_task_state, get_project_table
from app.utils.s3 import download_file
from app.utils.sqs import pull_one_message
from app.utils.task_states_const import task_states


def flip_the_image(task: dict[str, str]) -> None:
    file = download_file(task['file_path_orig'])
    process_image(file)
    pass


def main(*args) -> dict:
    if args:
        print("event = {}".format(args[0]))
    print(f"args: {args}")
    message = pull_one_message()
    task_id = json.loads(message.body)["task_id"]
    table = get_project_table()
    task = update_task_state(task_id, task_states.in_progress, table=table, return_values='ALL_NEW')

    try:
        flip_the_image(task)
    except Exception as e:
        print(e)
        update_task_state(task_id, task_states.crashed, table=table)
        res_task = task_states.crashed
    else:
        update_task_state(task_id, task_states.finished, table=table)
        res_task = task_states.finished

    dropped = message.delete()
    return {
        "status": 200,
        "task_id": task_id,
        "task": res_task,
        "dropped": bool(dropped)
    }


if __name__ == "__main__":
    flip_the_image({
        'file_name': 'reddit.wallpaper.png',
        'file_path_edited': '',
        'file_path_orig': 'upload_images/pgjmdiwegt/reddit.wallpaper.png',
        'state': 'in progress',
        'task_id': 'upload_images/pgjmdiwegt/reddit.wallpaper.png'
    })
