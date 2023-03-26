from fastapi import APIRouter

healthcheck = APIRouter(prefix='/healthcheck', tags=[""])


@healthcheck.get("/")
async def root():
    return {"status": "OK"}
