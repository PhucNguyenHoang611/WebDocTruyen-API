from fastapi import APIRouter, Depends
from models.rating import Rating
from services.rating import get_ratings, get_user_ratings, create_rating, update_rating, delete_rating
from middleware.auth import validate_token

router = APIRouter()

@router.get("/getAllRatings/{story_id}")
def get_all_ratings(story_id: str):
    return get_ratings(story_id)

@router.get("/getAllUserRatings/{user_id}", dependencies=[Depends(validate_token)])
def get_all_user_ratings(user_id: str):
    return get_user_ratings(user_id)

@router.post("/createRating", dependencies=[Depends(validate_token)])
def create_new_rating(rating: Rating):
    return create_rating(rating)

@router.put("/updateRating", dependencies=[Depends(validate_token)])
def update_rating_information(rating: Rating):
    return update_rating(rating)

@router.delete("/deleteRating/{rating_id}", dependencies=[Depends(validate_token)])
def delete_rating_by_id(rating_id: str):
    return delete_rating(rating_id)