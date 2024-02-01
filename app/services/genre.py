from config.database import dynamodb
from models.genre import Genre
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError

table = dynamodb.Table("Genres")

def get_genres():
    try:
        response = table.scan(
            AttributesToGet=[
                "genre_id",
                "name",
                "description"
            ]
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def get_genre(id: str):
    try:
        response = table.get_item(
            Key={
                "genre_id": id
            }
        )
        if "Item" in response:
            return response["Item"]
        else:
            return JSONResponse(content="Genre not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def create_genre(genre: Genre):
    try:
        item = Genre(
            name=genre.name,
            description=genre.description
        ).dict()

        table.put_item(Item=item)
        return JSONResponse(content=item, status_code=201)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def update_genre(genre: Genre):
    try:
        item = table.get_item(
            Key={
                "genre_id": genre.genre_id
            }
        )

        if "Item" in item:
            table.update_item(
                Key={
                    "genre_id": genre.genre_id
                },
                UpdateExpression="set #name=:name, #description=:description",
                ExpressionAttributeNames={
                    "#name": "name",
                    "#description": "description"
                },
                ExpressionAttributeValues={
                    ":name": genre.name,
                    ":description": genre.description
                }
            )
            return JSONResponse(content="Update genre successfully", status_code=200)
        else:
            return JSONResponse(content="Genre not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def delete_genre(id: str):
    try:
        item = table.get_item(
            Key={
                "genre_id": id
            }
        )

        if "Item" not in item:
            return JSONResponse(content="Genre not found", status_code=404)
        else:
            table.delete_item(
                Key={
                    "genre_id": id
                }
            )
            return JSONResponse(content="Delete genre successfully", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)