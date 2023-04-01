import boto3
from boto3_type_annotations import sqs

from app.settings import settings
from app.utils import config
import ujson as json


def get_queue() -> sqs.Queue:
    return boto3.resource('sqs', **config).get_queue_by_name(QueueName=settings.queue_name)


def push_sqs_message(data: dict, queue: sqs.Queue = None) -> None:
    if queue is None:
        queue = get_queue()
    queue.send_message(MessageBody=json.dumps(data))
