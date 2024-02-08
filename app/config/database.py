import os
from pathlib import Path
from dotenv import load_dotenv
from boto3 import resource

base_dir = Path(__file__).parent.parent.parent
load_dotenv(base_dir.joinpath(".env"))

dynamodb = resource("dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION_NAME")
)

tables = [
    {
        "TableName": "Stories",
        "KeySchema": [
            {
                "AttributeName": "story_id",
                "KeyType": "HASH"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "story_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "title",
                "AttributeType": "S"
            },
            {
                "AttributeName": "author",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "TitleIndex",
                "KeySchema": [
                    {
                        "AttributeName": "title",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": [
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
                        "created_at"
                    ]
                }
            },
            {
                "IndexName": "AuthorIndex",
                "KeySchema": [
                    {
                        "AttributeName": "author",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": [
                        "title",
                        "synopsis",
                        "cover_image_url",
                        "genres",
                        "tags",
                        "chapters_count",
                        "status",
                        "views",
                        "rating",
                        "total_votes",
                        "created_at"
                    ]
                }
            }
        ]
    },
    {
        "TableName": "Users",
        "KeySchema": [
            {
                "AttributeName": "user_id",
                "KeyType": "HASH"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "user_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "email",
                "AttributeType": "S"
            },
            {
                "AttributeName": "fullname",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "EmailIndex",
                "KeySchema": [
                    {
                        "AttributeName": "email",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": [
                        "password",
                        "fullname",
                        "role",
                        "is_verified",
                        "verification_key"
                    ]
                }
            },
            {
                "IndexName": "FullnameIndex",
                "KeySchema": [
                    {
                        "AttributeName": "fullname",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": [
                        "email",
                        "password",
                        "role",
                        "is_verified",
                        "verification_key"
                    ]
                }
            }
        ]
    },
    {
        "TableName": "Genres",
        "KeySchema": [
            {
                "AttributeName": "genre_id",
                "KeyType": "HASH"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "genre_id",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": []
    },
    {
        "TableName": "Tags",
        "KeySchema": [
            {
                "AttributeName": "tag_id",
                "KeyType": "HASH"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "tag_id",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": []
    },
    {
        "TableName": "Chapters",
        "KeySchema": [
            {
                "AttributeName": "chapter_id",
                "KeyType": "HASH"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "chapter_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "story_id",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "StoryIndex",
                "KeySchema": [
                    {
                        "AttributeName": "story_id",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": [
                        "chapter_number",
                        "title",
                        "content_url",
                        "created_at"
                    ]
                }
            }
        ]
    },
    {
        "TableName": "ViewedChapters",
        "KeySchema": [
            {
                "AttributeName": "user_id",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "chapter_id",
                "KeyType": "RANGE"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "user_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "chapter_id",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": []
    },
    {
        "TableName": "FavoriteStories",
        "KeySchema": [
            {
                "AttributeName": "user_id",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "story_id",
                "KeyType": "RANGE"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "user_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "story_id",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": []
    },
    {
        "TableName": "Ratings",
        "KeySchema": [
            {
                "AttributeName": "rating_id",
                "KeyType": "HASH"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "rating_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "user_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "story_id",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "UserIndex",
                "KeySchema": [
                    {
                        "AttributeName": "user_id",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": [
                        "story_id",
                        "rating",
                        "content",
                        "time"
                    ]
                }
            },
            {
                "IndexName": "StoryIndex",
                "KeySchema": [
                    {
                        "AttributeName": "story_id",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": [
                        "user_id",
                        "rating",
                        "content",
                        "time"
                    ]
                }
            }
        ]
    },
    {
        "TableName": "Comments",
        "KeySchema": [
            {
                "AttributeName": "comment_id",
                "KeyType": "HASH"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "comment_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "user_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "story_id",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "UserIndex",
                "KeySchema": [
                    {
                        "AttributeName": "user_id",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": [
                        "story_id",
                        "content",
                        "time"
                    ]
                }
            },
            {
                "IndexName": "StoryIndex",
                "KeySchema": [
                    {
                        "AttributeName": "story_id",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": [
                        "user_id",
                        "content",
                        "time"
                    ]
                }
            }
        ]
    },
    {
        "TableName": "Responses",
        "KeySchema": [
            {
                "AttributeName": "response_id",
                "KeyType": "HASH"
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "response_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "parent_id",
                "AttributeType": "S"
            }
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "ParentIndex",
                "KeySchema": [
                    {
                        "AttributeName": "parent_id",
                        "KeyType": "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "INCLUDE",
                    "NonKeyAttributes": [
                        "user_id",
                        "content",
                        "time"
                    ]
                }
            }
        ]
    }
]

def check_table_exists(table_name: str) -> bool:
    try:
        dynamodb.Table(table_name).table_status
    except Exception as e:
        print(e)
        return False
    return True

def create_tables():
    try:
        for table in tables:
            if table["GlobalSecondaryIndexes"] == []:
                
                if not check_table_exists(table["TableName"]):
                    dynamodb.create_table(
                        TableName=table["TableName"],
                        KeySchema=table["KeySchema"],
                        AttributeDefinitions=table["AttributeDefinitions"],
                        BillingMode="PAY_PER_REQUEST"
                    )
            
            else:
                
                if not check_table_exists(table["TableName"]):

                    dynamodb.create_table(
                        TableName=table["TableName"],
                        KeySchema=table["KeySchema"],
                        AttributeDefinitions=table["AttributeDefinitions"],
                        GlobalSecondaryIndexes=table["GlobalSecondaryIndexes"],
                        BillingMode="PAY_PER_REQUEST"
                    )
    except Exception as e:
        print(e)