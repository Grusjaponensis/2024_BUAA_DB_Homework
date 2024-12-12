from fastapi import APIRouter

from app.api.routes import (
    activity, login, user, post, cat, 
    volunteer, donation
)

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/users")
api_router.include_router(post.router, prefix="/posts", tags=["posts"])
api_router.include_router(cat.router, prefix="/cats", tags=["cats"])
api_router.include_router(activity.router, prefix="/activities", tags=["activities"])
api_router.include_router(volunteer.router, prefix="/volunteers")
api_router.include_router(donation.router , prefix="/donations", tags=["donations"])