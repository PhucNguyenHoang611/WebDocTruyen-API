from fastapi import APIRouter, Depends
from models.chapter import Chapter
from services.chapter import get_chapters, get_chapter, create_chapter, update_chapter, delete_chapter, delete_chapters
from middleware.auth import validate_token_admin

router = APIRouter()

@router.get("/getAllChapters/{story_id}")
def get_all_chapters(story_id: str):
    return get_chapters(story_id)

@router.get("/getChapterById/{chapter_id}")
def get_chapter_by_id(chapter_id: str):
    return get_chapter(chapter_id)

@router.post("/createChapter", dependencies=[Depends(validate_token_admin)])
def create_new_chapter(chapter: Chapter):
    return create_chapter(chapter)

@router.put("/updateChapter", dependencies=[Depends(validate_token_admin)])
def update_chapter_information(chapter: Chapter):
    return update_chapter(chapter)

@router.delete("/deleteChapter/{chapter_id}", dependencies=[Depends(validate_token_admin)])
def delete_chapter_by_id(chapter_id: str):
    return delete_chapter(chapter_id)

@router.delete("/deleteChapters/{story_id}", dependencies=[Depends(validate_token_admin)])
def delete_all_chapters_by_story_id(story_id: str):
    return delete_chapters(story_id)