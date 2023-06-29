from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.stats import StatsCard
from src.atcoder import Atcoder
from src.model import StatsOption

app = FastAPI()


@app.get("/stats/{username}", response_class=HTMLResponse)
async def stats(username: str, width: Optional[int] = None, height: Optional[int] = None):
    ac = Atcoder(username)
    option = StatsOption()
    if width: option.width = width
    if height: option.height = height
    card = StatsCard(ac.fetch_data(), option)
    return card.render()
