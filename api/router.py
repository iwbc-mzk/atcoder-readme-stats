from typing import Optional
import io

from fastapi import FastAPI
from fastapi.responses import Response

from src.stats import StatsCard, StatsOption
from src.atcoder import Atcoder
from src.themes import THEMES
from src.const import ONE_DAY_SECOND


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

    headers = {
        "Cache-Control": f"""
            max-age={ONE_DAY_SECOND // 2},
            stale-while-revalidate={ONE_DAY_SECOND},
            s-maxage={ONE_DAY_SECOND}
        """,
    }

    return Response(content=svg, headers=headers, media_type="image/svg+xml")
