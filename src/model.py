from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class UserData(BaseModel):
    id: str
    rank: int = 0
    rating: int = 0
    highest_rating: int = 0
    rated_matches: int = 0
    last_competed: Optional[datetime] = None
