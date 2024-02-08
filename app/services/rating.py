from config.database import dynamodb
from models.rating import Rating
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError

table = dynamodb.Table("Ratings")

def get_ratings(story_id: str):
    try:
        response = table.query(
            IndexName="StoryIndex",
            KeyConditionExpression="#story_id=:story_id",
            ExpressionAttributeNames={
                "#story_id": "story_id"
            },
            ExpressionAttributeValues={
                ":story_id": story_id
            },
            ProjectionExpression="rating_id, user_id, rating, content, time"
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def get_user_ratings(user_id: str):
    try:
        response = table.query(
            IndexName="UserIndex",
            KeyConditionExpression="#user_id=:user_id",
            ExpressionAttributeNames={
                "#user_id": "user_id"
            },
            ExpressionAttributeValues={
                ":user_id": user_id
            },
            ProjectionExpression="rating_id, story_id, rating, content, time"
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def create_rating(rating: Rating):
    try:
        item = Rating(
            user_id=rating.user_id,
            story_id=rating.story_id,
            rating=rating.rating,
            content=rating.content
        ).dict()

        table.put_item(Item=item)
        return JSONResponse(content=item, status_code=201)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def update_rating(rating: Rating):
    try:
        item = table.get_item(
            Key={
                "rating_id": rating.rating_id
            }
        )
        if "Item" in item:
            table.update_item(
                Key={
                    "rating_id": rating.rating_id
                },
                UpdateExpression="set #rating=:rating, #content=:content",
                ExpressionAttributeNames={
                    "#rating": "rating",
                    "#content": "content"
                },
                ExpressionAttributeValues={
                    ":rating": rating.rating,
                    ":content": rating.content
                }
            )
            return JSONResponse(content="Update rating successfully", status_code=200)
        else:
            return JSONResponse(content="Rating not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def delete_rating(id: str):
    try:
        response = table.get_item(
            Key={
                "rating_id": id
            }
        )
        if "Item" in response:
            table.delete_item(
                Key={
                    "rating_id": id
                }
            )
            return JSONResponse(content="Delete rating successfully", status_code=200)
        else:
            return JSONResponse(content="Rating not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)