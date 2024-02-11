from config.database import dynamodb
from models.story import Story
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
from decimal import Decimal

table = dynamodb.Table("Stories")
table_genres = dynamodb.Table("Genres")
table_tags = dynamodb.Table("Tags")

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
                "total_votes",
                "created_at"]
        )

        for story in response["Items"]:
            genres = []
            for genre_id in story["genres"]:
                genre = table_genres.get_item(
                    Key={
                        "genre_id": genre_id
                    }
                )
                genres.append(genre["Item"])
            story["genres"] = genres

            tags = []
            for tag_id in story["tags"]:
                tag = table_tags.get_item(
                    Key={
                        "tag_id": tag_id
                    }
                )
                tags.append(tag["Item"])
            story["tags"] = tags

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
            genres = []
            for genre_id in response["Item"]["genres"]:
                genre = table_genres.get_item(
                    Key={
                        "genre_id": genre_id
                    }
                )
                genres.append(genre["Item"])
            response["Item"]["genres"] = genres

            tags = []
            for tag_id in response["Item"]["tags"]:
                tag = table_tags.get_item(
                    Key={
                        "tag_id": tag_id
                    }
                )
                tags.append(tag["Item"])
            response["Item"]["tags"] = tags

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
            status=story.status
        ).dict()

        item["rating"] = Decimal(str(item["rating"]))
        table.put_item(Item=item)
        
        return JSONResponse(content={
            "story_id": item["story_id"],
            "title": item["title"],
            "synopsis": item["synopsis"],
            "cover_image_url": item["cover_image_url"],
            "author": item["author"],
            "genres": item["genres"],
            "tags": item["tags"],
            "chapters_count": item["chapters_count"],
            "status": item["status"],
            "views": item["views"],
            "rating": 0,
            "total_votes": item["total_votes"],
            "created_at": item["created_at"]
        }, status_code=201)
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
            table.update_item(
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
                    ":rating": Decimal(str(story.rating)),
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
            return JSONResponse(content="Update story successfully", status_code=200)
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
            table.delete_item(
                Key={
                    "story_id": id
                }
            )
            return JSONResponse(content="Delete story successfully", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)