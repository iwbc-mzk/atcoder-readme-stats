from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class UserData(BaseModel):
    id: str
    rank: Optional[int] = None
    rating: Optional[int] = None
    highest_rating: Optional[int] = None
    rated_matches: Optional[int] = None
    last_competed: Optional[datetime] = None


class StatsOption(BaseModel):
    width: int = 400
    height: int = 200
    hide: set[str] = set()
