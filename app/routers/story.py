from fastapi import APIRouter
from models.story import Story
from services.story import get_stories
from middleware.auth import validate_token
from fastapi import Depends

router = APIRouter()

@router.get("/getAllStories", dependencies=[Depends(validate_token)])
def get_all_stories():
    return get_stories()