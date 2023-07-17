from typing import Optional, Union, Literal
import io

from fastapi import FastAPI
from fastapi.responses import Response

from src.stats import StatsCard, StatsOption
from src.atcoder import Atcoder as atcoder
from src.themes import THEMES
from src.const import ONE_DAY_SECOND

Auto = Literal["auto"]


app = FastAPI()


@app.get("/stats/{username}")
async def stats(
    # path parameter
    username: str,
    # query parameter
    width: Optional[Union[int, Auto]] = None,
    height: Optional[Union[int, Auto]] = None,
    hide: Optional[str] = None,  # ex: hide=rating,last_competed
    theme: Optional[str] = None,
    show_history: Optional[Union[bool, int]] = False,
):
    option = StatsOption()
    if width:
        option.width = width
    if height:
        option.height = height
    if hide:
        option.hide = set(hide.split(","))
    if theme:
        option.theme = THEMES[theme] if theme in THEMES else THEMES["default"]
    if show_history:
        option.show_history = show_history

    try:
        userdata = atcoder.fetch_userdata(username, need_compe=bool(show_history))
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
