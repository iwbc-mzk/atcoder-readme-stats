from typing import Any

from src.model import UserData, StatsOption
from src.utils import get_rating_color


class StatsCard:
    def __init__(self, userdata: UserData, option: StatsOption = StatsOption()) -> None:
        self._userdata = userdata
        self._option = option

    def _field_to_label(self, field: str) -> str:
        key_label_map = {
            "id": "ID",
            "rank": "Rank",
            "rating": "Rating",
            "highest_rating": "Highest Rating",
            "rated_matches": "Rated Matches",
            "last_competed": "Last Competed",
        }

        return key_label_map[field]

    def _statsitems(self) -> list[tuple[str, Any]]:
        statsItems = []
        for key, val in self._userdata.dict().items():
            if key in self._option.hide:
                continue

            label = self._field_to_label(key)
            if key == "last_competed":
                val = val.strftime("%Y/%m/%d")
            statsItems.append((label, val))

        return statsItems

    def _renderStats(self) -> str:
        stats_rows = [
            f"""
                 <tr class="fadein stats-row" style="animation-delay: {(i + 3) * 150}ms">
                    <td class="stats-cell">{label}:</td>
                    <td class="stats-cell">{val}</td>
                </tr>
                """
            for i, (label, val) in enumerate(self._statsitems())
        ]
        style = f"""
            .stats-row {{
                height: 22px;
            }}
            .stats-cell {{
                color: #434d58;
                font-size: 15px;
                font-weight: 600;
            }}
            .stats-cell:nth-child(2) {{
                text-align: right;
            }}
        """

        return f"""
            <table style="width: 100%">
                {"".join(stats_rows)}
            </table>
            <style>{style}</style>
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
                    background-image: radial-gradient(white 60%, transparent 61%),
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
                width: 90px;
                height: 90px;
                text-align: center;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .circle {{
                width: 100%;
                height: 100%;
                border-radius: 50%;
                background-image: radial-gradient(white 60%, transparent 61%), conic-gradient({color} var(--deg), {color}33 var(--deg) 360deg);
                display: flex;
                justify-content: center;
                align-items: center;
                animation-name: conic-gradient;
                animation-duration: 0.8s;
                animation-fill-mode: forwards;
            }}
            .rating {{
                font-size: 24px;
                font-weight: 800;
                color: #434d58;
            }}

            @keyframes conic-gradient {{
                {"".join(keyframes)}
            }}
        """
        return f"""
            <div class="container fadein">
                <div class="circle">
                    <div>
                        <span class="rating">{rating}</span>
                    </div>
                </div>
            </div>
            <style>{style}</style>
        """

    def render(self):
        style = f"""
            #svg-body {{
                margin: 0;
            }}
            #card {{
                width: {self._option.width}px;
                height: {self._option.height}px;
                
                display: flex;
                position: relative;
            }}
            #card::after {{
                content: "";
                border: 1px solid rgb(228, 226, 226);
                border-radius: 10px;
                position: absolute;
                top: 0;
                left: 0;
                width: calc(100% - 2px);
                height: calc(100% - 2px);
            }}
            #card-body {{
                margin: auto;
                width: calc(100% - 40px);
                height: calc(100% - 40px);
            }}
            #title {{
                color: #54AEFF;
                font-size: 20px;
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
            <svg version="1.1" width="{self._option.width}" height="{self._option.height}" viewBox="0 0 {self._option.width+5} {self._option.height+5}" xmlns="http://www.w3.org/2000/svg">
                <foreignObject width="{self._option.width}" height="{self._option.height}" requiredExtensions="http://www.w3.org/1999/xhtml">
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
                        <style>{style}</style>
                    </body>
                </foreignObject>
            </svg>
        """
