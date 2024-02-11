from config.database import dynamodb
from models.rating import Rating
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from decimal import Decimal

table = dynamodb.Table("Ratings")
table_stories = dynamodb.Table("Stories")

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
            }
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
            }
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

        item["rating"] = Decimal(str(item["rating"]))
        table.put_item(Item=item)
        update_story_rating(rating.story_id)
        
        return JSONResponse(content={
            "rating_id": item["rating_id"],
            "user_id": item["user_id"],
            "story_id": item["story_id"],
            "content": item["content"],
            "time": item["time"]
        }, status_code=201)
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
                    ":rating": Decimal(str(rating.rating)),
                    ":content": rating.content
                }
            )

            update_story_rating(rating.story_id)
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

            update_story_rating(response["Item"]["story_id"])
            return JSONResponse(content="Delete rating successfully", status_code=200)
        else:
            return JSONResponse(content="Rating not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def update_story_rating(story_id: str):
    try:
        response = table.query(
            IndexName="StoryIndex",
            KeyConditionExpression="#story_id=:story_id",
            ExpressionAttributeNames={
                "#story_id": "story_id"
            },
            ExpressionAttributeValues={
                ":story_id": story_id
            }
        )
        ratings = response["Items"]

        total_rating = 0
        for rating in ratings:
            total_rating += rating["rating"]
        average_rating = total_rating / len(ratings)

        table_stories.update_item(
            Key={
                "story_id": story_id
            },
            UpdateExpression="set #rating=:rating",
            ExpressionAttributeNames={
                "#rating": "rating"
            },
            ExpressionAttributeValues={
                ":rating": average_rating
            }
        )
        return JSONResponse(content="Update story rating successfully", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)