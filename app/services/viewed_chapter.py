from config.database import dynamodb
from models.viewed_chapter import ViewedChapter
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("ViewedChapters")
table_chapters = dynamodb.Table("Chapters")

def get_viewed_chapters(user_id: str):
    try:
        response = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
            ProjectionExpression="chapter_id, completed_date"
        )

        for item in response["Items"]:
            chapter_id = item["chapter_id"]
            chapter = table_chapters.get_item(Key={"chapter_id": chapter_id})
            item["chapter_details"] = chapter["Item"]

        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def get_viewed_chapters_by_story(user_id: str, story_id: str):
    try:
        response = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
            ProjectionExpression="chapter_id, completed_date"
        )

        for item in response["Items"]:
            chapter_id = item["chapter_id"]
            chapter = table_chapters.get_item(Key={"chapter_id": chapter_id})
            item["chapter_details"] = chapter["Item"]

        # Keep items where story_id is equal to the story_id passed in
        response["Items"] = [item for item in response["Items"] if item["chapter_details"]["story_id"] == story_id]

        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def create_viewed_chapter(viewed_chapter: ViewedChapter):
    try:
        item = ViewedChapter(
            user_id=viewed_chapter.user_id,
            chapter_id=viewed_chapter.chapter_id
        ).dict()

        table.put_item(Item=item)
        return JSONResponse(content=item, status_code=201)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def delete_viewed_chapter(user_id: str, chapter_id: str):
    try:
        table.delete_item(
            Key={
                "user_id": user_id,
                "chapter_id": chapter_id
            }
        )
        return JSONResponse(content=f"Viewed chapter {chapter_id} deleted", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def delete_viewed_chapters(user_id: str):
    try:
        response = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
            ProjectionExpression="chapter_id"
        )
        items = response["Items"]
        
        for item in items:
            table.delete_item(
                Key={
                    "user_id": user_id,
                    "chapter_id": item["chapter_id"]
                }
            )
        return JSONResponse(content=f"Viewed chapters for user {user_id} deleted", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)