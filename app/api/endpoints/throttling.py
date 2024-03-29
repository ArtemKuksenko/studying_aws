from fastapi import APIRouter
from datetime import datetime
from random import randint

throttling = APIRouter(prefix='/throttling', tags=[""])


UNIQUE_APP_NUNBER = randint(0, 100)
START_TIME = datetime.now()


@throttling.get("/app_number")
async def root():
    return {
        "app_number": UNIQUE_APP_NUNBER,
        "start_time": START_TIME,
        "version": 0.01
    }


async def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n < 0:
        raise ValueError(f"Fibonacci of {n}")
    return await fibonacci(n - 1) + await fibonacci(n-2)


@throttling.get("/fibonacci/{number}")
async def lazy_fibonacci(number: int):
    return await fibonacci(number)
