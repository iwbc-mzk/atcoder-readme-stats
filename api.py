from typing import Optional
import io

from fastapi import FastAPI
from fastapi.responses import Response

from src import StatsCard, Atcoder, StatsOption
from src.themes import THEMES


app = FastAPI()


@app.get("/stats/{username}")
async def stats(
    # path parameter
    username: str,
    # query parameter
    width: Optional[int] = None,
    height: Optional[int] = None,
    hide: Optional[str] = None,  # ex: hide=rating,last_competed
    theme: Optional[str] = "default",
):
    ac = Atcoder(username)

    option = StatsOption()
    if width:
        option.width = width
    if height:
        option.height = height
    if hide:
        option.hide = set(hide.split(","))
    if theme:
        option.theme = THEMES[theme] if theme in THEMES else THEMES["default"]

    try:
        userdata = ac.fetch_data()
    except ValueError as e:
        return Response(content=e.args[0], status_code=404)

    card = StatsCard(userdata, option)
    svg = io.BytesIO(bytes(card.render(), "utf-8")).getvalue()

    return Response(content=svg, media_type="image/svg+xml")
