from typing import Optional, Union, Literal
import io

from fastapi import FastAPI, Query
from fastapi.responses import Response
from pydantic import ValidationError

from src.cards.stats import StatsCard, StatsOption
from src.cards.heatmap import HeatmapCard, HeatmapOption, Type as HeatmapType
from src.cards.error import ErrorCard
from src.atcoder import Atcoder as atcoder
from src.atcoder_problems import AtcoderProblems as ap
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
    show_history: Optional[Union[int, bool]] = False,
    show_icons: Optional[bool] = False,
    disable_animations: Optional[bool] = False,
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
    if show_icons:
        option.show_icons = show_icons
    if disable_animations:
        option.disable_animations = disable_animations

    try:
        userdata = atcoder.fetch_userdata(username, need_compe=bool(show_history))
    except ValueError as e:
        card = ErrorCard(e.args[0], e.args[1])
        svg = io.BytesIO(bytes(card.render(), "utf-8")).getvalue()
        headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
        }
        return Response(content=svg, headers=headers, media_type="image/svg+xml")

    card = StatsCard(userdata, option)
    svg = io.BytesIO(bytes(card.render(), "utf-8")).getvalue()

    headers = {
        "Cache-Control": f"max-age={ONE_DAY_SECOND // 2},stale-while-revalidate={ONE_DAY_SECOND},s-maxage={ONE_DAY_SECOND}",
    }

    return Response(content=svg, headers=headers, media_type="image/svg+xml")


@app.get("/heatmap/{username}")
async def heatmap(
    # path parameter
    username: str,
    # query parameter
    width: Optional[Union[int, Auto]] = None,
    height: Optional[Union[int, Auto]] = None,
    theme: Optional[str] = None,
    type: Optional[HeatmapType] = None,
    title_lines: Optional[int] = Query(default=None, ge=1),
    disable_animations: Optional[bool] = False,
):
    option = HeatmapOption()
    if width:
        option.width = width
    if height:
        option.height = height
    if theme:
        option.theme = THEMES[theme] if theme in THEMES else THEMES["default"]
    if type:
        option.type = type
    if title_lines:
        option.title_lines = title_lines
    if disable_animations:
        option.disable_animations = disable_animations

    try:
        submissions = ap.fetch_submissions(username)
    except ValidationError as e:
        err = e.errors()[0]
        card = ErrorCard(f'Location: {err.get("loc")}, Input: {err.get("input")}', err.get("msg"))
        headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
        }
    except Exception as e:
        card = ErrorCard(*e.args)
        headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
        }
    else:
        card = HeatmapCard(username, submissions, option)
        headers = {
            "Cache-Control": f"max-age={ONE_DAY_SECOND // 2},stale-while-revalidate={ONE_DAY_SECOND},s-maxage={ONE_DAY_SECOND}",
        }

    svg = io.BytesIO(bytes(card.render(), "utf-8")).getvalue()
    return Response(content=svg, headers=headers, media_type="image/svg+xml")
