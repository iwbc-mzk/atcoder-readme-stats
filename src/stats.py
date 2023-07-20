from typing import Any, Union, Literal
import html

from pydantic import BaseModel

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


KEY_LABEL_MAP = {
    "id": "ID",
    "rank": "Rank",
    "rating": "Rating",
    "highest_rating": "Highest Rating",
    "rated_matches": "Rated Matches",
    "last_competed": "Last Competed",
}


class StatsCard:
    def __init__(self, userdata: UserData, option: StatsOption = StatsOption()) -> None:
        self._userdata = userdata
        self._option = option

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
                 <tr class="fadein stats-row" style="animation-delay: {(i + 3) * 150}ms">
                    <td class="stats-cell" id="{stat.key}-label">
                        {f'<div class="icon">{get_icon(stat.key)}</div>' if self._option.show_icons else ""}
                        <div>{stat.label}:</div>
                    </td>
                    <td class="stats-cell" id="{stat.key}-value">{stat.value}</td>
                </tr>
                """
            for i, stat in enumerate(stats)
        ]
        style = f"""
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
        """

        return f"""
            <table style="width: 100%">
                {"".join(stats_rows)}
            </table>
            <style id="stats-style">{style}</style>
        """

    def _renderRatingCircle(self, rating: int) -> str:
        color = get_rating_color(rating)
        deg = 360 * (rating % 400) // 400

        # 暫定対応
        # できれば@propertyやanimationを使いたい
        keyframes = []
        N = 30
        for i in range(N + 1):
            prop = f"""
                {i * 100 // N}% {{
                    background-image: radial-gradient({self._option.theme.background_color} 60%, transparent 61%),
                    conic-gradient({color} {i * deg/N}deg, {color}33 {i * deg/N}deg 360deg);
                }}
            """
            keyframes.append(prop)

        style = f"""
            /*
            これを使ってランクサークルのアニメーションができそうだが上手くいかない
            @property --deg {{
                syntax: "&lt;angle&gt;"
                inherites: false;
                initial-value: 0deg
            }}
            @keyframes conic-gradient {{
                0% {{
                    --deg: 0deg;
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
            }}
            .rating {{
                color: {color};
            }}
            .rating-label {{
                font-size: 16px;
                font-weight: 600;
            }}
            .rating-text {{
                font-size: 24px;
                font-weight: 800;
            }}

            @keyframes conic-gradient {{
                {"".join(keyframes)}
            }}
        """
        return f"""
            <div class="container fadein">
                <div class="circle">
                    <div class="rating">
                        <span class="rating-label">Rating</span>
                        <br />
                        <span class="rating-text">{rating}</span>
                    </div>
                </div>
            </div>
            <style id="rating-circle-style">{style}</style>
        """

    def _render_competitions_history(self, row_num):
        competitions = sorted(
            self._userdata.competitions_history, key=lambda x: x.date, reverse=True
        )

        competitions_rows = []
        for i, compe in enumerate(competitions):
            if i >= row_num:
                break

            competitions_rows.append(
                f"""
                <tr class="compe-row">
                    <td class="compe-val val-date">{compe.date.strftime("%Y-%m-%d")}</td>
                    <td class="compe-val"><div class="val-contest">{html.escape(compe.contest)}</div></td>
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

        style = f"""
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

        return f"""
            <table class="compe-table">
                <colgroup>
                    <col width="20%" />
                    <col width="50%" />
                    <col width="15%" />
                    <col width="15%" />
                </colgroup>
                <tr>
                    <th>Date</th>
                    <th>Contest</th>
                    <th>Rank</th>
                    <th>Perf</th>
                </tr>
                {"".join(competitions_rows)}
            </table>
            <style>{style}</style>
        """

    def render(self):
        width = self._option.width
        height = self._option.height
        theme = self._option.theme
        show_history = bool(self._option.show_history)

        compe_history_num = len(self._userdata.competitions_history)
        history_row_num = (
            min(self._option.show_history, compe_history_num)
            if type(self._option.show_history) == int
            else min(3, compe_history_num)
        )

        viewbox_height = 200
        if height == "auto" and show_history:
            viewbox_height += 36 * (history_row_num + 1) + 15

        style = f"""
            #svg-body {{
                margin: 0;
                font-family: {theme.font_family};
                color: {theme.text_color};
                height: 100%;
                width: 100%;
            }}
            #card {{
                width: calc(100% - 2px);
                height: calc(100% - 2px);
                
                display: flex;
                position: relative;
                background-color: {theme.background_color};

                border: 1px solid rgb(228, 226, 226);
                border-radius: 10px;
            }}
            #card-body {{
                margin: 20px;
                width: calc(100% - 40px);
                height: calc(100% - 40px);
                display: flex;
                flex-direction: column;
            }}
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
        """
        return f"""
            <svg version="1.1" 
                viewBox="0 0 450 {viewbox_height}"
                xmlns="http://www.w3.org/2000/svg"
                {f'width="{width}"' if type(width) == int else ""}
                {f'height="{height}"' if type(height) == int else ""}
            >
                <foreignObject width="450" height="{viewbox_height}" requiredExtensions="http://www.w3.org/1999/xhtml">
                    <body id="svg-body" xmlns="http://www.w3.org/1999/xhtml">
                        <div id="card">
                            <div id="card-body">
                                <div id="title" class="fadein">{self._userdata.id}'s Atcoder Stats</div>
                                <div id="stats-body">
                                    <div id="stats">
                                        {self._renderStats()}
                                    </div>
                                    <div id="rank-circle">
                                        {self._renderRatingCircle(self._userdata.rating)}
                                    </div>
                                </div>
                                {f'''
                                    <div class="border"></div>
                                    <div id="competitions-history-body">
                                        {self._render_competitions_history(history_row_num)}
                                    </div>''' if show_history else ""}
                            </div>
                        </div>
                        <style id="main-style">{style}</style>
                    </body>
                </foreignObject>
            </svg>
        """
