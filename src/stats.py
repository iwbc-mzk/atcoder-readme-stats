from typing import Any

from src.model import UserData, StatsOption


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
        stats = [
            f"""
                 <tr class="fadein" style="animation-delay: {(i + 3) * 150}ms">
                    <td>{label}:</td>
                    <td>{val}</td>
                </tr>
                """
            for i, (label, val) in enumerate(self._statsitems())
        ]

        return f"<table>{''.join(stats)}</table>"

    def render(self):
        print(*UserData.__fields__.keys())
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
            tr {{
                height: 22px;
            }}
            td {{
                color: #434d58;
                font-size: 14px;
                font-weight: 600;
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
                                <table>
                                    {self._renderStats()}
                                </table>
                            </div>
                        </div>
                        <style>{style}</style>
                    </body>
                </foreignObject>
            </svg>
        """
