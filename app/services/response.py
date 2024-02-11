from config.database import dynamodb
from models.response import Response
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError

table = dynamodb.Table("Responses")

def get_responses(parent_id: str):
    try:
        response = table.query(
            IndexName="ParentIndex",
            KeyConditionExpression="#parent_id=:parent_id",
            ExpressionAttributeNames={
                "#parent_id": "parent_id"
            },
            ExpressionAttributeValues={
                ":parent_id": parent_id
            }
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def create_response(response: Response):
    try:
        item = Response(
            parent_id=response.parent_id,
            user_id=response.user_id,
            content=response.content
        ).dict()

        table.put_item(Item=item)
        return JSONResponse(content=item, status_code=201)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def update_response(response: Response):
    try:
        item = table.get_item(
            Key={
                "response_id": response.response_id
            }
        )

        if "Item" in item:
            table.update_item(
                Key={
                    "response_id": response.response_id
                },
                UpdateExpression="set #content=:content",
                ExpressionAttributeValues={
                    ":content": response.content
                },
                ExpressionAttributeNames={
                    "#content": "content"
                }
            )
            return JSONResponse(content="Update response successfully", status_code=200)
        else:
            return JSONResponse(content="Response not found", status_code=404)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def delete_response(id: str):
    try:
        response = table.get_item(
            Key={
                "response_id": id
            }
        )

        if "Item" not in response:
            return JSONResponse(content="Response not found", status_code=404)
        else:
            table.delete_item(
                Key={
                    "response_id": id
                }
            )
            return JSONResponse(content="Response deleted", status_code=200)
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)