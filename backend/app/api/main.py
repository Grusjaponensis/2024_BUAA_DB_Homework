from fastapi import APIRouter

from app.api.routes import login, user, post

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/users")
api_router.include_router(post.router, prefix="/posts", tags=["posts"])