from routers import story, user, genre, tag, chapter, viewed_chapter, favorite_story
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(genre.router, prefix="/genres", tags=["Genres"])
api_router.include_router(tag.router, prefix="/tags", tags=["Tags"])
api_router.include_router(story.router, prefix="/stories", tags=["Stories"])
api_router.include_router(chapter.router, prefix="/chapters", tags=["Chapters"])
api_router.include_router(viewed_chapter.router, prefix="/viewedChapters", tags=["Viewed Chapters"])
api_router.include_router(favorite_story.router, prefix="/favoriteStories", tags=["Favorite Stories"])