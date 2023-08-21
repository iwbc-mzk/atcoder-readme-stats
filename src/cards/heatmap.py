from typing import Any, Union, Literal, List
import datetime

from pydantic import BaseModel

from src.cards.card import Card
from src.atcoder_problems import Submission
from src.themes import Theme, THEMES
from src.utils import date_range

Auto = Literal["auto"]
Type = Literal["all_submissions", "all_ac", "unique_ac", "max_difficulty"]


class StatsItem(BaseModel):
    key: str
    label: str
    value: Any


class HeatmapOption(BaseModel):
    width: Union[int, Auto] = "auto"
    height: Union[int, Auto] = "auto"
    theme: Theme = THEMES["default"]
    type: Type = "all_submissions"


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
        self._weeks_num = 24

        super().__init__(
            width=self._option.width,
            height=self._option.height,
            viewbox_height=200,
            theme=self._option.theme,
        )

    def _get_cell_color(self, percentile: float) -> str:
        if percentile == 0.0:
            return "#EBEDF0"
        else:
            if 0 < percentile <= 0.25:
                return "#C6E48B"
            elif 0.25 < percentile <= 0.50:
                return "#7BC96F"
            elif 0.50 < percentile <= 0.75:
                return "#239A3B"
            else:
                return "#196127"

    def _render_title(self) -> str:
        return f"""
            <div id="title" class="fadein">{self._username}'s Atcoder Submission Heatmap</div>
        """

    def _render_body(self):
        now = datetime.date.today()
        today = datetime.datetime(now.year, now.month, now.day)
        to_ = today + datetime.timedelta(days=(7 - today.isoweekday()))
        from_ = to_ - datetime.timedelta(weeks=self._weeks_num)

        submissions_by_day: List[tuple[datetime.datetime, List[Submission]]] = []
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

        week_labels = ["", "Mo", "", "We", "", "Fr", ""]
        month_labels = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]

        month_cells = ['<div class="heatmap-cell month-label"></div>']
        cells = []
        for i, (date, submissions) in enumerate(submissions_by_day):
            if date > today:
                break

            cells.append(
                f"""
                <div 
                    class="heatmap-cell" 
                    id="{date.strftime("%Y-%m-%d")}" 
                    style="background-color: {self._get_cell_color(len(submissions)/max_sub_cnt)};
                "></div>
            """
            )
            if i % 7 == 0:
                next_month_first = datetime.datetime(date.year, date.month + 1, 1)
                if next_month_first - date < datetime.timedelta(days=7):
                    month_cells.append(
                        f"""
                            <div class="heatmap-cell label-text month-label">
                                {month_labels[next_month_first.month - 1]}
                            </div>
                        """
                    )
                else:
                    month_cells.append('<div class="heatmap-cell month-label"></div>')

        return f"""
            <div id="heatmap-container">
                <div id="month-labels">{"".join(month_cells)}</div>
                <div id="heatmap">
                    <div id="week-labels">
                        {"".join(f'<div class="heatmap-cell label-text week-label">{label}</div>' for label in week_labels)}
                    </div>
                    <div id="heatmap-cells">
                        {"".join(cells)}
                    </div>
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
                flex-direction: column;
            }}
            #heatmap {{
                margin: 0px;
                display: flex;
                width: 100%;
                height: calc(100% * 7 / 8);
            }}
            #week-labels {{
                display: flex;
                flex-direction: column;
                height: 100%;
                width: calc(100% / ({self._weeks_num} + 1))
            }}
            #heatmap-cells {{
                display: flex;
                flex-direction: column;
                flex-wrap: wrap;
                height: 100%;
                width: calc(100% * {self._weeks_num} / ({self._weeks_num} + 1));
            }}
            #month-labels {{
                display: flex;
                flex-direction: row;
                width: 100%;
                height: calc(100% * 1 / 8);
            }}
            .heatmap-cell {{
                height: calc(100% / 7);
                outline: 1px solid {self._option.theme.background_color};
                width: calc(100% / {self._weeks_num + 1});
            }}
            .label-text {{
                font-size: 13px;
            }}
            .month-label {{
                text-align: left;
                text-indent: 2px;
                line-height: 1;
                outline: 0;
            }}
            .week-label {{
                text-align: center;
                position: relative;
                right: 5px;
                outline: 0;
                line-height: 1;
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
