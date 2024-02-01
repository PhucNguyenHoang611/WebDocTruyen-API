from routers import story, user, genre, tag
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(story.router, prefix="/stories", tags=["Stories"])
api_router.include_router(genre.router, prefix="/genres", tags=["Genres"])
api_router.include_router(tag.router, prefix="/tags", tags=["Tags"])