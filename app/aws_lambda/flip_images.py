import json

from app.utils.dynamo_db import update_task_state, get_project_table
from app.utils.sqs import pull_one_message
from app.utils.task_states_const import task_states


def main(*args) -> dict:
    if args:
        print("event = {}".format(args[0]))
    print(f"args: {args}")
    message = pull_one_message()
    task_id = json.loads(message.body)["task_id"]
    table = get_project_table()
    update_task_state(task_id, task_states.in_progress, table=table)

    try:
        pass
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
    main()
