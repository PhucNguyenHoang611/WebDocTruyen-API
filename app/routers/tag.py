from fastapi import APIRouter, Depends
from models.tag import Tag
from services.tag import get_tags, get_tag, create_tag, update_tag, delete_tag
from middleware.auth import validate_token_admin

router = APIRouter()

@router.get("/getAllTags")
def get_all_tags():
    return get_tags()

@router.get("/getTagById/{tag_id}")
def get_tag_by_id(tag_id: str):
    return get_tag(tag_id)

@router.post("/createTag", dependencies=[Depends(validate_token_admin)])
def create_new_tag(tag: Tag):
    return create_tag(tag)

@router.put("/updateTag", dependencies=[Depends(validate_token_admin)])
def update_tag_information(tag: Tag):
    return update_tag(tag)

@router.delete("/deleteTag/{tag_id}", dependencies=[Depends(validate_token_admin)])
def delete_tag_by_id(tag_id: str):
    return delete_tag(tag_id)