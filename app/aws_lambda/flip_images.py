import json

from app.utils.sqs import pull_one_message


def main(*args) -> dict:
    if args:
        print("event = {}".format(args[0]))
    print(f"args: {args}")
    message = pull_one_message()
    task_id = json.loads(message.body)["task_id"]

    dropped = message.delete()
    return {"status": 200, "task_id": task_id, "dropped": bool(dropped)}


if __name__ == "__main__":
    main()
