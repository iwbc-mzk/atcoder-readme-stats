import datetime

from bs4 import BeautifulSoup
import pytest

from src.cards.heatmap import HeatmapCard, HeatmapOption
from src.atcoder_problems import Submission
from src.themes import THEMES
from tests.utils import get_property_from_css, serialize_css

NOW = datetime.datetime.now()

USER_NAME = "iwbc_mzk"
SUBMISSIONS = [
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(NOW.timestamp()),
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
            "epoch_second": int(NOW.timestamp()),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_b",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(NOW.timestamp()),
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
            "epoch_second": int(NOW.timestamp()),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_c",
            "result": "AC",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int(NOW.timestamp()),
            "execution_time": 55,
            "id": 44708254,
            "language": "Python (PyPy 3.10-v7.3.12)",
            "length": 262,
            "point": 100,
            "problem_id": "abc315_d",
            "result": "WA",
            "user_id": "iwbc_mzk",
        }
    ),
    Submission(
        **{
            "contest_id": "abc315",
            "epoch_second": int((NOW - datetime.timedelta(days=1)).timestamp()),
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
            "epoch_second": int((NOW - datetime.timedelta(days=1)).timestamp()),
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
            "epoch_second": int((NOW - datetime.timedelta(days=1)).timestamp()),
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
            "epoch_second": int((NOW - datetime.timedelta(days=2)).timestamp()),
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
            "epoch_second": int((NOW - datetime.timedelta(days=2)).timestamp()),
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
            "epoch_second": int((NOW - datetime.timedelta(days=3)).timestamp()),
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
        assert soup.find(id="title").string == f"{USER_NAME}'s Atcoder Submission"

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
        today = datetime.datetime(year=NOW.year, month=NOW.month, day=NOW.day)
        weekend = today + datetime.timedelta(days=(7 - (today.isoweekday() % 7)))
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

    @pytest.mark.parametrize("theme", ["default", "darcula"])
    def test_theme_option(self, theme):
        option = HeatmapOption()

        theme = THEMES[theme]
        option.theme = theme
        heatmap_card = HeatmapCard(
            username=USER_NAME, submissions=SUBMISSIONS, option=option
        )
        soup = BeautifulSoup(heatmap_card.render(), "html.parser")

        styles = serialize_css(soup.find("style", id="main-style").string)

        # Font Family
        font_falmily = get_property_from_css(styles, "#svg-body", "font-family")
        assert font_falmily
        assert font_falmily == theme.font_family

        # Background Color
        background_color = get_property_from_css(styles, "#card", "background-color")
        assert background_color
        assert background_color == theme.background_color

        # Title Color
        title_color = get_property_from_css(styles, "#title", "color")
        assert title_color
        assert title_color == theme.title_color

        # Text Color
        text_color = get_property_from_css(styles, "#svg-body", "color")
        assert text_color
        assert text_color == theme.text_color

    @pytest.mark.parametrize(
        "type_, count, title",
        [
            ("all", "5", f"{USER_NAME}'s Atcoder Submission"),
            ("ac", "4", f"{USER_NAME}'s Atcoder AC Submission"),
            ("unique_ac", "3", f"{USER_NAME}'s Atcoder Unique AC Submission"),
        ],
    )
    def test_type_option(self, type_, count, title):
        option = HeatmapOption()

        option.type = type_
        heatmap_card = HeatmapCard(
            username=USER_NAME, submissions=SUBMISSIONS, option=option
        )
        soup = BeautifulSoup(heatmap_card.render(), "html.parser")

        # Title
        assert soup.find(id="title").string == title

        # Submission Count
        heatmap_cells = soup.find(id="heatmap-cells").find_all(class_="heatmap-cell")
        last_cell = heatmap_cells[-1]
        assert last_cell.attrs.get("_test_submission_count", "") == count

    @pytest.mark.parametrize(
        "title_lines, height", [(-1, 200), (0, 200), (1, 200), (2, 227), (10, 443)]
    )
    def test_title_lines_option(self, title_lines, height):
        option = HeatmapOption()

        option.title_lines = title_lines
        heatmap_card = HeatmapCard(
            username=USER_NAME, submissions=SUBMISSIONS, option=option
        )
        soup = BeautifulSoup(heatmap_card.render(), "html.parser")

        svg = soup.find("svg")

        assert svg.attrs["viewbox"] == f"0 0 450 {height}"

        foreignobject = svg.find("foreignobject")
        assert foreignobject.attrs.get("width", "") == "450"
        assert foreignobject.attrs.get("height", "") == str(height)

        styles = serialize_css(soup.find("style", id="main-style").string)

        container_height = get_property_from_css(styles, "#title-container", "height")
        assert container_height
        assert container_height == "auto"

        title_wrap = get_property_from_css(styles, "#title", "text-wrap")
        assert title_wrap
        assert title_wrap == "wrap"
