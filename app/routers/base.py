from routers import story, user
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(story.router, prefix="/stories", tags=["Stories"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])