import json

import boto3
from botocore.client import Config

from app.settings import settings
from app.utils import config

CONFIG = {
    "config": Config(signature_version='s3v4', s3={'addressing_style': 'path'}),
    "region_name": "ap-south-1",
}


def get_message():
    sqs = boto3.resource('sqs', **config)
    queue = sqs.get_queue_by_name(QueueName=settings.queue_name)

    message = queue.receive_messages(MaxNumberOfMessages=1)
    if not message:
        raise ValueError(f"No message in SQS {settings.queue_name}")
    return message[0]


def main(*args) -> dict:
    if args:
        print("event = {}".format(args[0]))
    print(f"args: {args}")
    message = get_message()
    task_id = json.loads(message.body)["task_id"]

    dropped = message.delete()
    return {"status": 200, "task_id": task_id, "dropped": bool(dropped)}


if __name__ == "__main__":
    main()
