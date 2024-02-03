from fastapi import APIRouter, Depends
from models.viewed_chapter import ViewedChapter
from services.viewed_chapter import get_viewed_chapters, create_viewed_chapter, delete_viewed_chapter, delete_viewed_chapters
from middleware.auth import validate_token

router = APIRouter()

@router.get("/getViewedChapters/{user_id}", dependencies=[Depends(validate_token)])
def get_viewed_chapters_by_user_id(user_id: str):
    return get_viewed_chapters(user_id)

@router.post("/createViewedChapter", dependencies=[Depends(validate_token)])
def create_new_viewed_chapter(viewed_chapter: ViewedChapter):
    return create_viewed_chapter(viewed_chapter)

@router.delete("/deleteViewedChapter/{user_id}/{chapter_id}", dependencies=[Depends(validate_token)])
def delete_viewed_chapter_by_user_id_and_chapter_id(user_id: str, chapter_id: str):
    return delete_viewed_chapter(user_id, chapter_id)

@router.delete("/deleteViewedChapters/{user_id}", dependencies=[Depends(validate_token)])
def delete_all_viewed_chapters_by_user_id(user_id: str):
    return delete_viewed_chapters(user_id)