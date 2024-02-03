from pydantic import BaseModel

class FavoriteStory(BaseModel):
    user_id: str
    story_id: str