import string
import random

from botocore.client import Config
from app.settings import settings


config = {
    "config": Config(signature_version='s3v4', s3={'addressing_style': 'path'}),
    "region_name": settings.region_name,
}


def get_random_string(n: int = 10) -> str:
    """
    Generate random string of len = n
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(n))
