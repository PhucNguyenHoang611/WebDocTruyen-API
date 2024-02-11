from config.database import dynamodb
from models.chapter import Chapter
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("Chapters")

def get_chapters(story_id: str):
    try:
        response = table.query(
            IndexName="StoryIndex",
            KeyConditionExpression=Key("story_id").eq(story_id),
            ProjectionExpression="chapter_id, chapter_number, title, content_url, created_at"
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def get_latest_chapter(story_id: str):
    try:
        response = table.query(
            IndexName="StoryIndex",
            KeyConditionExpression=Key("story_id").eq(story_id),
            ProjectionExpression="chapter_id, chapter_number, title, content_url, created_at"
        )

        if "Items" in response and len(response["Items"]) > 0:
            response["Items"].sort(key=lambda x: x["created_at"], reverse=True)
            return response["Items"][0]
        else:
            return JSONResponse(content="Chapter not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def get_chapter(id: str):
    try:
        response = table.get_item(
            Key={
                "chapter_id": id
            }
        )
        if "Item" in response:
            return response["Item"]
        else:
            return JSONResponse(content="Chapter not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def create_chapter(chapter: Chapter):
    try:
        item = Chapter(
            story_id=chapter.story_id,
            chapter_number=chapter.chapter_number,
            title=chapter.title,
            content_url=chapter.content_url
        ).dict()

        table.put_item(Item=item)
        return JSONResponse(content=item, status_code=201)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def update_chapter(chapter: Chapter):
    try:
        table.update_item(
            Key={
                "chapter_id": chapter.chapter_id
            },
            UpdateExpression="set #story_id=:story_id, #chapter_number=:chapter_number, #title=:title, #content_url=:content_url",
            ExpressionAttributeValues={
                ":story_id": chapter.story_id,
                ":chapter_number": chapter.chapter_number,
                ":title": chapter.title,
                ":content_url": chapter.content_url
            },
            ExpressionAttributeNames={
                "#story_id": "story_id",
                "#chapter_number": "chapter_number",
                "#title": "title",
                "#content_url": "content_url"
            }
        )
        return JSONResponse(content="Update chapter successfully", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def delete_chapter(id: str):
    try:
        item = table.get_item(
            Key={
                "chapter_id": id
            }
        )

        if "Item" not in item:
            return JSONResponse(content="Chapter not found", status_code=404)
        else:
            table.delete_item(
                Key={
                    "chapter_id": id
                }
            )
            return JSONResponse(content="Delete chapter successfully", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def delete_chapters(story_id: str):
    try:
        chapters = get_chapters(story_id)
        if len(chapters) == 0:
            return JSONResponse(content="Chapters not found", status_code=404)
        else:
            for chapter in chapters:
                table.delete_item(
                    Key={
                        "chapter_id": chapter["chapter_id"]
                    }
                )
            return JSONResponse(content="Delete all chapters successfully", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)