from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.stats import StatsCard
from src.atcoder import Atcoder

app = FastAPI()


@app.get("/stats/{username}", response_class=HTMLResponse)
async def stats(username: str, width: int = None, height: int = None):
    ac = Atcoder(username)
    card = StatsCard(ac.fetch_data())
    return card.render()
