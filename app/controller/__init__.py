from botocore.client import Config
from app.settings import settings


config = {
    "config": Config(signature_version='s3v4', s3={'addressing_style': 'path'}),
    "region_name": settings.region_name,
}
