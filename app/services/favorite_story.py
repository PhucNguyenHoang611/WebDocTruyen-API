from config.database import dynamodb
from models.favorite_story import FavoriteStory
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("FavoriteStories")

def get_favorite_stories(user_id: str):
    try:
        response = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
            ProjectionExpression="story_id"
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def create_favorite_story(favorite_story: FavoriteStory):
    try:
        item = FavoriteStory(
            user_id=favorite_story.user_id,
            story_id=favorite_story.story_id
        ).dict()

        table.put_item(Item=item)
        return JSONResponse(content=item, status_code=201)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def delete_favorite_story(user_id: str, story_id: str):
    try:
        table.delete_item(
            Key={
                "user_id": user_id,
                "story_id": story_id
            }
        )
        return JSONResponse(content=f"Favorite story {story_id} deleted", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def delete_favorite_stories(user_id: str):
    try:
        response = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
            ProjectionExpression="story_id"
        )
        for item in response["Items"]:
            table.delete_item(
                Key={
                    "user_id": user_id,
                    "story_id": item["story_id"]
                }
            )
        return JSONResponse(content=f"Favorite stories for user {user_id} deleted", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)