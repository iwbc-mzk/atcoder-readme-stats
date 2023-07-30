from typing import Any, Union, Literal, List
import datetime

from pydantic import BaseModel

from src.cards.card import Card
from src.atcoder_problems import Submission
from src.themes import Theme, THEMES
from src.utils import date_range

Auto = Literal["auto"]
Target = Literal["all_sub", "all_ac", "unique_ac", "diff"]


class StatsItem(BaseModel):
    key: str
    label: str
    value: Any


class HeatmapOption(BaseModel):
    width: Union[int, Auto] = "auto"
    height: Union[int, Auto] = "auto"
    hide: set[str] = set()
    theme: Theme = THEMES["default"]
    target: Target = "all_sub"


class HeatmapCard(Card):
    def __init__(
        self,
        username: str,
        submissions: List[Submission],
        option: HeatmapOption = HeatmapOption(),
    ) -> None:
        self._username = username
        self._submissions = submissions
        self._option = option

        super().__init__(
            width=self._option.width,
            height=self._option.height,
            viewbox_height=300,
            theme=self._option.theme,
        )

    def _get_cell_color(self, percentile: float) -> str:
        if percentile == 0.0:
            return "#EBEDF0"
        else:
            base_color = "#196127"
            if 0 < percentile <= 0.10:
                transparent = "1A"
            elif 0.10 < percentile <= 0.20:
                transparent = "33"
            elif 0.20 < percentile <= 0.30:
                transparent = "4D"
            elif 0.30 < percentile <= 0.40:
                transparent = "66"
            elif 0.40 < percentile <= 0.50:
                transparent = "80"
            elif 0.50 < percentile <= 0.60:
                transparent = "99"
            elif 0.60 < percentile <= 0.70:
                transparent = "B3"
            elif 0.70 < percentile <= 0.80:
                transparent = "CC"
            elif 0.80 < percentile <= 0.90:
                transparent = "E6"
            else:
                transparent = "FF"

            return base_color + transparent

    def _render_title(self) -> str:
        return f"""
            <div id="title" class="fadein">{self._username}'s Atcoder Submission Heatmap</div>
        """

    def _render_body(self):
        now = datetime.date.today()
        today = datetime.datetime(now.year, now.month, now.day)
        to_ = today + datetime.timedelta(days=(7 - today.isoweekday()))
        from_ = to_ - datetime.timedelta(weeks=15)

        submissions_by_day = []
        last_sub_idx = 0
        max_sub_cnt = 0
        for date in date_range(from_, to_):
            submissions = []
            from_unix = date.timestamp()
            end_unix = (date + datetime.timedelta(days=1)).timestamp()
            for i in range(last_sub_idx, len(self._submissions)):
                submission = self._submissions[i]
                if from_unix <= submission.epoch_second < end_unix:
                    submissions.append(submission)
                elif end_unix <= submission.epoch_second:
                    last_sub_idx = i
                    break
            submissions_by_day.append((date, submissions))
            max_sub_cnt = max(max_sub_cnt, len(submissions))

        return f"""
            <div id="heatmap-container">
                <div id="heatmap">
                    {"".join(f'''
                        <div 
                            class="heatmap-cell" 
                            id="{date.strftime("%Y-%m-%d")}" 
                            style="background-color: {self._get_cell_color(len(submissions)/max_sub_cnt)};
                        "></div>'''
                        for date, submissions in submissions_by_day)
                    }
                </div>
            </div>
        """

    def _styles(self) -> str:
        theme = self._option.theme

        return f"""
            #title {{
                color: {theme.title_color};
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 10px;
            }}
            .fadein {{
                opacity: 0;
                animation-name: fadein;
                animation-duration: 0.8s;
                animation-timing-function: ease-in-out;
                animation-fill-mode: forwards;
            }}
            
            #heatmap-container {{
                width: 100%;
                height: 100%;
                display: flex;
            }}
            #heatmap {{
                margin: 0px;
                display: flex;
                flex-direction: column;
                flex-wrap: wrap;
                width: 100%;
                height: 100%;
            }}
            .heatmap-cell {{
                height: 13%;
                border: 1px solid white;
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
