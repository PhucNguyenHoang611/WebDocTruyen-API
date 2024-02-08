from fastapi import APIRouter, Depends
from models.response import Response
from services.response import get_responses, create_response, update_response, delete_response
from middleware.auth import validate_token

router = APIRouter()

@router.get("/getAllResponses/{parent_id}")
def get_all_responses(parent_id: str):
    return get_responses(parent_id)

@router.post("/createResponse", dependencies=[Depends(validate_token)])
def create_new_response(response: Response):
    return create_response(response)

@router.put("/updateResponse", dependencies=[Depends(validate_token)])
def update_response_information(response: Response):
    return update_response(response)

@router.delete("/deleteResponse/{response_id}", dependencies=[Depends(validate_token)])
def delete_response_by_id(response_id: str):
    return delete_response(response_id)