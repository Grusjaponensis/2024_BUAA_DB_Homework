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
if settings.ALL_COR_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALL_COR_ORIGINS,
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
    if not os.path.exists(settings.UPLOAD_AVATAR_FOLDER):
        os.makedirs(settings.UPLOAD_AVATAR_FOLDER)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    

