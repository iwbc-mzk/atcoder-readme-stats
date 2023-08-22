import datetime

from bs4 import BeautifulSoup
import pytest

from src.cards.heatmap import HeatmapCard, HeatmapOption
from src.atcoder_problems import Submission


USER_NAME = "iwbc_mzk"
SUBMISSIONS = [
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(datetime.datetime.now().timestamp()),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_a",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(datetime.datetime.now().timestamp()),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_a",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(datetime.datetime.now().timestamp()),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_a",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(datetime.datetime.now().timestamp()),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_a",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(
                (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
            ),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_a",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(
                (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
            ),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_a",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(
                (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
            ),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_a",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(
                (datetime.datetime.now() - datetime.timedelta(days=2)).timestamp()
            ),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_a",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(
                (datetime.datetime.now() - datetime.timedelta(days=2)).timestamp()
            ),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_a",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(
                (datetime.datetime.now() - datetime.timedelta(days=3)).timestamp()
            ),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_a",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
]


class TestHeatmapCard:
    def test_render_with_default_option(self):
        option = HeatmapOption()
        heatmap_card = HeatmapCard(
            username=USER_NAME, submissions=SUBMISSIONS, option=option
        )
        soup = BeautifulSoup(heatmap_card.render(), "html.parser")

        svg = soup.find("svg")

        # default width is not set
        assert "width" not in svg.attrs
        # default height is not set
        assert "width" not in svg.attrs
        # viewbox width and height are 450 and 200
        assert svg.attrs["viewbox"] == "0 0 450 200"

        # Title
        assert (
            soup.find(id="title").string == f"{USER_NAME}'s Atcoder Submission Heatmap"
        )

        # Week Label
        week_labels = soup.find_all(id="week-labels")
        for i, label in enumerate(week_labels):
            label = label.string
            if i in [0, 2, 4, 6]:
                assert label is None
            elif i == 1:
                assert label == "Mo"
            elif i == 3:
                assert label == "We"
            elif i == 5:
                assert label == "Fr"
            else:
                assert False

        # Heatmap Cell
        heatmap_cells = soup.find(id="heatmap-cells").find_all(class_="heatmap-cell")
        begin_cell, end_cell = heatmap_cells[0], heatmap_cells[-1]
        now = datetime.datetime.now()
        today = datetime.datetime(year=now.year, month=now.month, day=now.day)
        weekend = today + datetime.timedelta(days=(7 - today.isoweekday()))
        begin_day = weekend - datetime.timedelta(weeks=24)
        # 24週前の日曜日から今日まで
        assert begin_cell.attrs.get("id", "") == begin_day.strftime("%Y-%m-%d")
        assert end_cell.attrs.get("id", "") == today.strftime("%Y-%m-%d")

        # セルの色
        for color, delta in zip(
            ["#196127", "#239A3B", "#7BC96F", "#C6E48B", "#EBEDF0"], [0, 1, 2, 3, 4]
        ):
            cell = heatmap_cells[-(1 + delta)]
            assert f"background-color: {color}" in cell.attrs.get("style", "")

    @pytest.mark.parametrize(
        "width, height",
        [
            (100, None),
            (400, None),
            (700, None),
            ("auto", None),
            (None, 100),
            (None, 400),
            (None, 700),
            (None, "auto"),
            (100, 400),
            (500, 100),
            ("auto", "auto"),
        ],
    )
    def test_width_height_option(self, width, height):
        option = HeatmapOption()
        if width:
            option.width = width
        if height:
            option.height = height
        heatmap_card = HeatmapCard(
            username=USER_NAME, submissions=SUBMISSIONS, option=option
        )
        soup = BeautifulSoup(heatmap_card.render(), "html.parser")
        svg = soup.find("svg")

        if isinstance(width, int):
            assert "width" in svg.attrs
            assert width == int(svg.attrs.get("width", -1))
        else:
            assert "width" not in svg.attrs

        if isinstance(height, int):
            assert "height" in svg.attrs
            assert height == int(svg.attrs.get("height", -1))
        else:
            assert "height" not in svg.attrs

        foreignobject = svg.find("foreignobject")
        assert foreignobject.attrs.get("width", "") == "450"
        assert foreignobject.attrs.get("height", "") == "200"
