import logging

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.init_data import init


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    logging.info("Creating initial data")
    init()
    logging.info("Initial data created")
    
    import os
    paths_to_create = [
        settings.UPLOAD_AVATAR_FOLDER,
        settings.UPLOAD_POST_IMAGE_FOLDER
    ]
    for path in paths_to_create:
        os.makedirs(path, exist_ok=True) # set exist_ok to True to avoid error when folder already exists
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    

