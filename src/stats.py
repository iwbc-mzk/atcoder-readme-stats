from typing import Any, Union, Literal

from pydantic import BaseModel

from src.atcoder import UserData
from src.utils import get_rating_color
from src.themes import Theme, THEMES

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
            if key in ({"id", "rating"} | self._option.hide) or key not in KEY_LABEL_MAP:
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
                    <td class="stats-cell" id="{stat.key}-label">{stat.label}:</td>
                    <td class="stats-cell" id="{stat.key}-value">{stat.value}</td>
                </tr>
                """
            for i, stat in enumerate(stats)
        ]
        style = f"""
            .stats-row {{
                height: 28px;
            }}
            .stats-cell {{
                font-size: 16px;
                font-weight: 700;
            }}
            .stats-cell:nth-child(2) {{
                text-align: right;
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

    def render(self):
        width = self._option.width
        height = self._option.height
        theme = self._option.theme

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
                margin: auto;
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
                viewBox="0 0 450 200"
                xmlns="http://www.w3.org/2000/svg"
                {f'width="{width}"' if type(width) == int else ""}
                {f'height="{height}"' if type(height) == int else ""}
            >
                <foreignObject width="450" height="200" requiredExtensions="http://www.w3.org/1999/xhtml">
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
                            </div>
                        </div>
                        <style id="main-style">{style}</style>
                    </body>
                </foreignObject>
            </svg>
        """
