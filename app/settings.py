from pydantic import BaseSettings


class Settings(BaseSettings):
    region_name: str = "ap-south-1"
    bucket_name: str = 'processing-pictures-bucket'

    port: int = 8080


settings = Settings()
