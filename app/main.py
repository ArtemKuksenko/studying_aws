from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.routers import api_router

app = FastAPI(
    openapi_url='/docs/openapi.json'
)

app.include_router(api_router)
app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
