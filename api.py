from typing import Optional
import io

from fastapi import FastAPI
from fastapi.responses import Response

from src.stats import StatsCard
from src.atcoder import Atcoder
from src.model import StatsOption

app = FastAPI()


@app.get("/stats/{username}")
async def stats(
    username: str, width: Optional[int] = None, height: Optional[int] = None
):
    ac = Atcoder(username)
    option = StatsOption()
    if width:
        option.width = width
    if height:
        option.height = height
    card = StatsCard(ac.fetch_data(), option)
    svg = io.BytesIO(bytes(card.render(), "utf-8")).getvalue()

    return Response(content=svg, media_type="image/svg+xml")
