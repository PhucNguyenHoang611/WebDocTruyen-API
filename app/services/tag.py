from config.database import dynamodb
from models.tag import Tag
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError

table = dynamodb.Table("Tags")

def get_tags():
    try:
        response = table.scan(
            AttributesToGet=[
                "tag_id",
                "name",
                "description"
            ]
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def get_tag(id: str):
    try:
        response = table.get_item(
            Key={
                "tag_id": id
            }
        )
        if "Item" in response:
            return response["Item"]
        else:
            return JSONResponse(content="Tag not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
    
def create_tag(tag: Tag):
    try:
        item = Tag(
            name=tag.name,
            description=tag.description
        ).dict()

        table.put_item(Item=item)
        return JSONResponse(content=item, status_code=201)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def update_tag(tag: Tag):
    try:
        item = table.get_item(
            Key={
                "tag_id": tag.tag_id
            }
        )

        if "Item" in item:
            table.update_item(
                Key={
                    "tag_id": tag.tag_id
                },
                UpdateExpression="set #name=:name, #description=:description",
                ExpressionAttributeNames={
                    "#name": "name",
                    "#description": "description"
                },
                ExpressionAttributeValues={
                    ":name": tag.name,
                    ":description": tag.description
                }
            )
            return JSONResponse(content="Tag updated successfully", status_code=200)
        else:
            return JSONResponse(content="Tag not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def delete_tag(id: str):
    try:
        response = table.get_item(
            Key={
                "tag_id": id
            }
        )
        if "Item" in response:
            table.delete_item(
                Key={
                    "tag_id": id
                }
            )
            return JSONResponse(content="Tag deleted successfully", status_code=200)
        else:
            return JSONResponse(content="Tag not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)