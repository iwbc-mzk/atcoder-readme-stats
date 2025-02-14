from typing import Any, Union, Literal
import html

from pydantic import BaseModel

from src.cards.card import Card
from src.atcoder import UserData
from src.utils import get_rating_color
from src.themes import Theme, THEMES
from src.icons import get_icon

Auto = Literal["auto"]


class StatsItem(BaseModel):
    key: str
    label: str
    value: Any


class StatsOption(BaseModel):
    width: Union[int, Auto] = "auto"
    height: Union[int, Auto] = "auto"
    hide: set[str] = set()
    theme: Theme = THEMES["default"]
    show_history: Union[int, bool] = False
    show_icons: bool = False
    disable_animations: bool = False


KEY_LABEL_MAP = {
    "id": "ID",
    "rank": "Rank",
    "rating": "Rating",
    "highest_rating": "Highest Rating",
    "rated_matches": "Rated Matches",
    "last_competed": "Last Competed",
}


class StatsCard(Card):
    def __init__(self, userdata: UserData, option: StatsOption = StatsOption()) -> None:
        self._userdata = userdata
        self._option = option

        self._prepare()

        super().__init__(
            width=self._option.width,
            height=self._option.height,
            viewbox_height=self._viewbox_height,
            theme=self._option.theme,
        )

    def _prepare(self) -> None:
        self._set_history_row_num()
        self._set_viewbox_height()

    def _set_history_row_num(self):
        compe_history_num = len(self._userdata.competitions_history)
        self._history_row_num = (
            min(self._option.show_history, compe_history_num)
            if type(self._option.show_history) == int
            else min(3, compe_history_num)
        )

    def _set_viewbox_height(self) -> None:
        # Need to execute _set_history_row_num first.
        self._viewbox_height = 200
        if self._option.height == "auto" and self._option.show_history:
            self._viewbox_height += 36 * (self._history_row_num + 1) + 15

    def _field_to_label(self, field: str) -> str:
        return KEY_LABEL_MAP[field]

    def _statsitems(self) -> list[StatsItem]:
        statsItems = []
        for key, val in self._userdata.model_dump().items():
            if (
                key in ({"id", "rating"} | self._option.hide)
                or key not in KEY_LABEL_MAP
            ):
                continue

            label = self._field_to_label(key)
            if key == "last_competed":
                val = val.strftime("%Y/%m/%d")
            statsItems.append(StatsItem(key=key, label=label, value=val))

        return statsItems

    def _renderStats(self) -> str:
        stats = self._statsitems()

        stats_rows = [
            f"""
                 <tr class="{"" if self._option.disable_animations else "fadein"} stats-row" style="animation-delay: {(i + 3) * 150}ms">
                    <td class="stats-cell">
                        {f'<div class="icon">{get_icon(stat.key)}</div>' if self._option.show_icons else ""}
                        <div id="{stat.key}-label">{stat.label}:</div>
                    </td>
                    <td class="stats-cell" id="{stat.key}-value">{stat.value}</td>
                </tr>
                """
            for i, stat in enumerate(stats)
        ]

        return f"""
            <table style="width: 100%">
                {"".join(stats_rows)}
            </table>
        """

    def _renderRatingCircle(self, rating: int) -> str:
        return f"""
            <div class="container {"" if self._option.disable_animations else "fadein"}">
                <div class="circle">
                    <div class="rating">
                        <span id="rating-label">Rating</span>
                        <br />
                        <span id="rating-value">{rating}</span>
                    </div>
                </div>
            </div>
        """

    def _render_competitions_history(self):
        competitions = sorted(
            self._userdata.competitions_history, key=lambda x: x.date, reverse=True
        )

        competitions_rows = []
        for i, compe in enumerate(competitions):
            if i >= self._history_row_num:
                break

            competitions_rows.append(
                f"""
                <tr class="{"" if self._option.disable_animations else "fadein"} compe-row" style="animation-delay: {(i + 8) * 150}ms">
                    <td class="compe-val val-date">{compe.date.strftime("%Y-%m-%d")}</td>
                    <td class="compe-val"><div class="val-contest">{html.escape(compe.contest_en if compe.contest_en else compe.contest_jp )}</div></td>
                    <td class="compe-val">{compe.rank}</td>
                    <td 
                        class="compe-val" 
                        {f'style="color: {get_rating_color(compe.performance)}"' if type(compe.performance) == int else ""}
                    >
                            {compe.performance if compe.performance else "-"}
                    </td>
                </tr>
            """
            )

        return f"""
            <table class="compe-table">
                <colgroup>
                    <col width="20%" />
                    <col width="50%" />
                    <col width="15%" />
                    <col width="15%" />
                </colgroup>
                <tr class="{"" if self._option.disable_animations else "fadein"}" style="animation-delay: {7 * 150}ms">
                    <th>Date</th>
                    <th>Contest</th>
                    <th>Rank</th>
                    <th>Perf</th>
                </tr>
                {"".join(competitions_rows)}
            </table>
        """

    def _render_title(self) -> str:
        return f"""
            <div id="title" class="{"" if self._option.disable_animations else "fadein"}">{self._userdata.id}'s Atcoder Stats</div>
        """

    def _render_body(self):
        show_history = bool(self._option.show_history)

        return f"""
            <div id="stats-body">
                <div id="stats">
                    {self._renderStats()}
                </div>
                {f'''
                    <div id="rank-circle">
                        {self._renderRatingCircle(self._userdata.rating)}
                    </div>
                 ''' if "rating" not in self._option.hide else ""}
            </div>
            {f'''
                <div class="border"></div>
                <div id="competitions-history-body">
                    {self._render_competitions_history()}
                </div>''' if show_history else ""}
        """

    def _styles(self) -> str:
        theme = self._option.theme

        color = get_rating_color(self._userdata.rating)
        deg = 360 * (self._userdata.rating % 400) // 400

        # 暫定対応
        # できれば@propertyやanimationを使いたい
        keyframes = []
        if not self._option.disable_animations:
            N = 30
            for i in range(N + 1):
                prop = f"""
                    {i * 100 // N}% {{
                        background-image: radial-gradient({self._option.theme.background_color} 60%, transparent 61%),
                        conic-gradient({color} {i * deg/N}deg, {color}33 {i * deg/N}deg 360deg);
                    }}
                """
                keyframes.append(prop)

        return f"""
            #title {{
                color: {theme.title_color};
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 10px;
            }}
            #stats-body {{
                display: flex;
                flex-direction: row;
            }}
            #stats {{
                width: 60%;
                margin: auto;
            }}
            #rank-circle {{
                width: 40%;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            #competitions-history-body {{
                width: 100%;
            }}
            .border {{
                height: 2px;
                background-color: rgb(228, 226, 226);
                margin: 5px 20px 0px;
            }}
            .fadein {{
                opacity: 0;
                animation-name: fadein;
                animation-duration: 0.8s;
                animation-timing-function: ease-in-out;
                animation-fill-mode: forwards;
            }}
            @keyframes fadein {{
                0% {{
                    opacity: 0;
                }}
                100% {{
                    opacity: 1;
                }}
            }}

            /* Stats */
            .stats-row {{
                height: 28px;
                display: flex;
            }}
            .stats-cell {{
                font-size: 16px;
                font-weight: 700;
                display: flex;
                margin: auto auto auto 0px;
            }}
            .stats-cell:nth-child(2) {{
                text-align: right;
                margin: auto 0px auto auto;
            }}
            .icon {{
                width: 18px;
                height: 18px;
                margin: auto 5px auto 0px;
                color: {self._option.theme.icon_color};
            }}

            /* Rating Circle */
            /*
            これを使ってランクサークルのアニメーションができそうだが上手くいかない
            @property --deg {{
                syntax: "&lt;angle&gt;"
                inherites: false;
                initial-value: 0deg
            }}
            @keyframes conic-gradient {{
                0% {{
                    --deg: f{f'{deg}deg' if self._option.disable_animations else "0deg"};
                }}
                100% {{
                    --deg: {deg}deg;
                }}
            }}
            */
            
            .container {{
                width: 95px;
                height: 95px;
                text-align: center;
                display: flex;
                justify-content: center;
                align-items: center;
                margin-left: 20px;
            }}
            .circle {{
                width: 100%;
                height: 100%;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
  
                animation-name: conic-gradient;
                animation-duration: 0.8s;
                animation-fill-mode: forwards;
                background-image: radial-gradient({self._option.theme.background_color} 60%, transparent 61%), conic-gradient({color} {deg}deg, {color}33 {deg}deg 360deg);
            }}
            .rating {{
                color: {color};
            }}
            #rating-label {{
                font-size: 16px;
                font-weight: 600;
            }}
            #rating-value {{
                font-size: 24px;
                font-weight: 800;
            }}

            @keyframes conic-gradient {{
                {"".join(keyframes)}
            }}

            /* Competition History */
            .compe-val {{
                font-size: 14px;
                font-weight: 700;
                text-align: center;
                padding: 0;
            }}
            .compe-table {{
                width: 100%;
                table-layout: fixed;
            }}
            .compe-table > tr > th {{
                height: 34px;
                font-size: 14px;
                padding: 0;
            }}
            .compe-row > td {{
                height: 34px;
            }}
            .val-date {{
                font-size: 12px;
            }}
            .val-contest {{
                font-size: 12px;
                text-align: left;
                overflow: hidden;
                display: -webkit-box;
                -webkit-box-orient: vertical;
                -webkit-line-clamp: 2;
            }}
        """
