from pydantic import BaseModel

class FavoriteStories(BaseModel):
    user_id: str
    story_id: str