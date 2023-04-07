import boto3
from boto3_type_annotations import sqs

from app.controller import config
from app.settings import settings
import ujson as json


def get_queue() -> sqs.Queue:
    return boto3.resource('sqs', **config).get_queue_by_name(QueueName=settings.queue_name)


def pull_one_message() -> sqs.Message:
    message = get_queue().receive_messages(MaxNumberOfMessages=1)
    if not message:
        raise ValueError(f"No message in SQS {settings.queue_name}")
    return message[0]


def push_sqs_message(data: dict, queue: sqs.Queue = None) -> None:
    if queue is None:
        queue = get_queue()
    queue.send_message(MessageBody=json.dumps(data))
