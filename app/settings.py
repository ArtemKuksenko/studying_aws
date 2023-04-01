from pydantic import BaseSettings


class Settings(BaseSettings):
    region_name: str = "ap-south-1"
    bucket_name: str = 'processing-pictures-bucket'
    dynamo_db_table_name: str = 'task'
    queue_name: str = 'flip-images-tasks-queue'

    port: int = 8080


settings = Settings()
