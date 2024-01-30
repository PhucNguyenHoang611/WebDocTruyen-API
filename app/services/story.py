from config.database import dynamodb
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