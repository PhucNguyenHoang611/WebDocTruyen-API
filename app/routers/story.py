from fastapi import APIRouter, Depends
from models.story import Story
from services.story import get_stories, get_story, create_story, update_story, delete_story
from middleware.auth import validate_token_admin

router = APIRouter()

@router.get("/getAllStories")
def get_all_stories():
    return get_stories()

@router.get("/getStoryById/{story_id}")
def get_story_by_id(story_id: str):
    return get_story(story_id)

@router.post("/createStory", dependencies=[Depends(validate_token_admin)])
def create_new_story(story: Story):
    return create_story(story)

@router.put("/updateStory", dependencies=[Depends(validate_token_admin)])
def update_story_information(story: Story):
    return update_story(story)

@router.delete("/deleteStory/{story_id}", dependencies=[Depends(validate_token_admin)])
def delete_story_by_id(story_id: str):
    return delete_story(story_id)