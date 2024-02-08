from fastapi import APIRouter, Depends
from models.comment import Comment
from services.comment import get_comments, get_user_comments, create_comment, update_comment, delete_comment
from middleware.auth import validate_token

router = APIRouter()

@router.get("/getAllComments/{story_id}")
def get_all_comments(story_id: str):
    return get_comments(story_id)

@router.get("/getAllUserComments/{user_id}", dependencies=[Depends(validate_token)])
def get_all_user_comments(user_id: str):
    return get_user_comments(user_id)

@router.post("/createComment", dependencies=[Depends(validate_token)])
def create_new_comment(comment: Comment):
    return create_comment(comment)

@router.put("/updateComment", dependencies=[Depends(validate_token)])
def update_comment_information(comment: Comment):
    return update_comment(comment)

@router.delete("/deleteComment/{comment_id}", dependencies=[Depends(validate_token)])
def delete_comment_by_id(comment_id: str):
    return delete_comment(comment_id)