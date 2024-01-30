from config.database import dynamodb
from models.story import Story
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("Stories")

def get_stories():
    try:
        response = table.scan(
            AttributesToGet=[
                "story_id",
                "title",
                "synopsis",
                "cover_image_url",
                "author",
                "genres",
                "tags",
                "chapters_count",
                "status",
                "views",
                "rating",
                "total_votes"]
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def get_story(id: str):
    try:
        response = table.get_item(
            Key={
                "story_id": id
            }
        )
        if "Item" in response:
            return response["Item"]
        else:
            return JSONResponse(content="Story not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def create_story(story: Story):
    try:
        item = Story(
            title=story.title,
            synopsis=story.synopsis,
            cover_image_url=story.cover_image_url,
            author=story.author,
            genres=story.genres,
            tags=story.tags,
            chapters_count=story.chapters_count,
            status=story.status,
            views=story.views,
            rating=story.rating,
            total_votes=story.total_votes
        ).dict()

        table.put_item(Item=item)
        return JSONResponse(content=item, status_code=201)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def update_story(story: Story):
    try:
        item = table.get_item(
            Key={
                "story_id": story.story_id
            }
        )

        if "Item" not in item:
            return JSONResponse(content="Story not found", status_code=404)
        else:
            response = table.update_item(
                Key={
                    "story_id": story.story_id
                },
                UpdateExpression="set #title=:title, #synopsis=:synopsis, #cover_image_url=:cover_image_url, #author=:author, #genres=:genres, #tags=:tags, #chapters_count=:chapters_count, #status=:status, #views=:views, #rating=:rating, #total_votes=:total_votes",
                ExpressionAttributeValues={
                    ":title": story.title,
                    ":synopsis": story.synopsis,
                    ":cover_image_url": story.cover_image_url,
                    ":author": story.author,
                    ":genres": story.genres,
                    ":tags": story.tags,
                    ":chapters_count": story.chapters_count,
                    ":status": story.status,
                    ":views": story.views,
                    ":rating": story.rating,
                    ":total_votes": story.total_votes
                },
                ExpressionAttributeNames={
                    "#title": "title",
                    "#synopsis": "synopsis",
                    "#cover_image_url": "cover_image_url",
                    "#author": "author",
                    "#genres": "genres",
                    "#tags": "tags",
                    "#chapters_count": "chapters_count",
                    "#status": "status",
                    "#views": "views",
                    "#rating": "rating",
                    "#total_votes": "total_votes"
                }
            )
            return JSONResponse(content=response, status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def delete_story(id: str):
    try:
        item = table.get_item(
            Key={
                "story_id": id
            }
        )

        if "Item" not in item:
            return JSONResponse(content="Story not found", status_code=404)
        else:
            response = table.delete_item(
                Key={
                    "story_id": id
                }
            )
            return JSONResponse(content=response, status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)