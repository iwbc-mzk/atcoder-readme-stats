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
class StatsOption(BaseModel):
    width: Optional[int] = 400
    height: Optional[int] = 200
    hide: Optional[set[str]] = {"id"}
