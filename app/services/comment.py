from config.database import dynamodb
from models.comment import Comment
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError

table = dynamodb.Table("Comments")

def get_comments(story_id: str):
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
            ProjectionExpression="comment_id, user_id, content, time"
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def get_user_comments(user_id: str):
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
            ProjectionExpression="comment_id, story_id, content, time"
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def create_comment(comment: Comment):
    try:
        item = Comment(
            user_id=comment.user_id,
            story_id=comment.story_id,
            content=comment.content
        ).dict()

        table.put_item(Item=item)
        return JSONResponse(content=item, status_code=201)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def update_comment(comment: Comment):
    try:
        item = table.get_item(
            Key={
                "comment_id": comment.comment_id
            }
        )

        if "Item" in item:
            table.update_item(
                Key={
                    "comment_id": comment.comment_id
                },
                UpdateExpression="set #content=:content",
                ExpressionAttributeValues={
                    ":content": comment.content
                },
                ExpressionAttributeNames={
                    "#content": "content"
                }
            )
            return JSONResponse(content="Update comment successfully", status_code=200)
        else:
            return JSONResponse(content="Comment not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def delete_comment(id: str):
    try:
        response = table.get_item(
            Key={
                "comment_id": id
            }
        )
        if "Item" not in response:
            return JSONResponse(content="Comment not found", status_code=404)
        else:
            table.delete_item(
                Key={
                    "comment_id": id
                }
            )
            return JSONResponse(content="Delete comment successfully", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)