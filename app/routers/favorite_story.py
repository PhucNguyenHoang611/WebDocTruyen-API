from fastapi import APIRouter, Depends
from models.favorite_story import FavoriteStory
from services.favorite_story import get_favorite_stories, create_favorite_story, delete_favorite_story, delete_favorite_stories
from middleware.auth import validate_token

router = APIRouter()

@router.get("/getFavoriteStories/{user_id}", dependencies=[Depends(validate_token)])
def get_favorite_stories_by_user_id(user_id: str):
    return get_favorite_stories(user_id)

@router.post("/createFavoriteStory", dependencies=[Depends(validate_token)])
def create_new_favorite_story(favorite_story: FavoriteStory):
    return create_favorite_story(favorite_story)

@router.delete("/deleteFavoriteStory/{user_id}/{story_id}", dependencies=[Depends(validate_token)])
def delete_favorite_story_by_user_id_and_story_id(user_id: str, story_id: str):
    return delete_favorite_story(user_id, story_id)

@router.delete("/deleteFavoriteStories/{user_id}", dependencies=[Depends(validate_token)])
def delete_favorite_stories_by_user_id(user_id: str):
    return delete_favorite_stories(user_id)