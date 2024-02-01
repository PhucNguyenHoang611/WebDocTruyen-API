from fastapi import APIRouter, Depends
from models.genre import Genre
from services.genre import get_genres, get_genre, create_genre, update_genre, delete_genre
from middleware.auth import validate_token_admin

router = APIRouter()

@router.get("/getAllGenres")
def get_all_genres():
    return get_genres()

@router.get("/getGenreById/{genre_id}")
def get_genre_by_id(genre_id: str):
    return get_genre(genre_id)

@router.post("/createGenre", dependencies=[Depends(validate_token_admin)])
def create_new_genre(genre: Genre):
    return create_genre(genre)

@router.put("/updateGenre", dependencies=[Depends(validate_token_admin)])
def update_genre_information(genre: Genre):
    return update_genre(genre)

@router.delete("/deleteGenre/{genre_id}", dependencies=[Depends(validate_token_admin)])
def delete_genre_by_id(genre_id: str):
    return delete_genre(genre_id)