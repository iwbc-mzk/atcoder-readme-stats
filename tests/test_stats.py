import datetime
from typing import Union, Literal, Optional

from bs4 import BeautifulSoup
import pytest

from src.cards.stats import StatsCard, StatsOption
from src.atcoder import UserData, Competition
from src.themes import THEMES
from src.utils import get_rating_color
from tests.utils import get_property_from_css, serialize_css


class TestStatsCard:
    userdata = UserData(
        id="test_user",
        rank=1000,
        rating=1450,
        highest_rating=400,
        rated_matches=90,
        last_competed=datetime.datetime(2023, 4, 10),
        competitions_history=[
            Competition(
                **{
                    "date": datetime.datetime(
                        2023,
                        6,
                        17,
                        22,
                        40,
                        tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)),
                    ),
                    "is_rated": True,
                    "contest_jp": "トヨタ自動車プログラミングコンテスト2023#3（AtCoder Beginner Contest 306）",
                    "contest_en": "Toyota Programming Contest 2023#3（AtCoder Beginner Contest 306）",
                    "rank": 2219,
                    "performance": None,
                    "new_rating": None,
                    "old_rating": None,
                }
            ),
            Competition(
                **{
                    "date": datetime.datetime(
                        2023,
                        6,
                        18,
                        23,
                        0,
                        tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)),
                    ),
                    "is_rated": True,
                    "contest_jp": "AtCoder Regular Contest 162",
                    "contest_en": "AtCoder Regular Contest 162",
                    "rank": 1253,
                    "performance": 1036,
                    "new_rating": 1000,
                    "old_rating": 900,
                }
            ),
            Competition(
                **{
                    "date": datetime.datetime(
                        2023,
                        6,
                        24,
                        22,
                        40,
                        tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)),
                    ),
                    "is_rated": True,
                    "contest_jp": "東京海上日動プログラミングコンテスト2023（AtCoder Beginner Contest 307）",
                    "contest_en": "Tokio Marine & Nichido Fire Insurance Programming Contest 2023（AtCoder Beginner Contest 307)",
                    "rank": 3814,
                    "performance": 647,
                    "new_rating": 772,
                    "old_rating": 842,
                }
            ),
            Competition(
                **{
                    "date": datetime.datetime(
                        2023,
                        7,
                        1,
                        22,
                        40,
                        tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)),
                    ),
                    "is_rated": True,
                    "contest_jp": "",
                    "contest_en": "Tokio Marine & Nichido Fire Insurance Programming Contest 2023（AtCoder Beginner Contest 308)",
                    "rank": 3814,
                    "performance": 100,
                    "new_rating": 300,
                    "old_rating": 317,
                }
            ),
        ],
    )

    def _check_competitions_history(
        self,
        show_history: Union[int, bool],
        height: Union[int, Literal["auto"]] = "auto",
    ):
        DEFAULT_ROWS_NUM = 3

        option = StatsOption()
        option.show_history = show_history
        if height:
            option.height = height
        stats_card = StatsCard(userdata=self.userdata, option=option)
        soup = BeautifulSoup(stats_card.render(), "html.parser")

        border = soup.find(class_="border")
        history = soup.find(id="competitions-history-body")
        if not bool(show_history):
            assert border is None
            assert history is None
            return

        assert border is not None
        assert history is not None

        if type(show_history) == int:
            compe_rows_num = min(show_history, len(self.userdata.competitions_history))
        else:
            compe_rows_num = DEFAULT_ROWS_NUM if show_history else 0
        compe_rows = history.find_all(class_="compe-row")
        assert len(compe_rows) == compe_rows_num

        # competitions history is displayed in descending order of contest date
        for compe, validator in zip(
            compe_rows, reversed(self.userdata.competitions_history)
        ):
            for i, val_cell in enumerate(compe.find_all(class_="compe-val")):
                val = val_cell.string
                if i == 0:
                    assert val == validator.date.strftime("%Y-%m-%d")
                elif i == 1:
                    assert (
                        val == validator.contest_en
                        if validator.contest_en
                        else validator.contest_jp
                    )
                elif i == 2:
                    assert int(val) == validator.rank if validator.rank else "-"
                else:
                    assert (
                        int(val) == validator.performance
                        if validator.performance
                        else "-"
                    )
                    if validator.performance:
                        color = get_rating_color(validator.performance)
                        val_cell.attrs["style"] = f"color: {color}"

        svg = soup.find("svg")
        if height == "auto" and bool(show_history):
            viewbox_height = 200 + 36 * (compe_rows_num + 1) + 15
            assert svg.attrs["viewbox"] == f"0 0 450 {viewbox_height}"
        else:
            assert svg.attrs["viewbox"] == "0 0 450 200"

    def test_render_with_default_option(self):
        option = StatsOption()
        stats_card = StatsCard(userdata=self.userdata, option=option)
        soup = BeautifulSoup(stats_card.render(), "html.parser")

        svg = soup.find("svg")

        # default width is not set
        assert "width" not in svg.attrs
        # default height is not set
        assert "width" not in svg.attrs
        # viewbox width and height are 450 and 200
        assert svg.attrs["viewbox"] == "0 0 450 200"

        # Title
        assert soup.find(id="title").string == f"{self.userdata.id}'s Atcoder Stats"

        # ID
        assert not soup.find(id="id-label")
        assert not soup.find(id="id-value")
        # Rating
        assert not soup.find(id="rating-label")
        assert not soup.find(id="rating-value")
        # Rank
        assert soup.find(id="rank-label").string == "Rank:"
        assert int(soup.find(id="rank-value").string) == self.userdata.rank
        # Highenst Rating
        assert soup.find(id="highest_rating-label").string == "Highest Rating:"
        assert (
            int(soup.find(id="highest_rating-value").string)
            == self.userdata.highest_rating
        )
        # Rated Matches
        assert soup.find(id="rated_matches-label").string == "Rated Matches:"
        assert (
            int(soup.find(id="rated_matches-value").string)
            == self.userdata.rated_matches
        )
        # Last Competed
        assert soup.find(id="last_competed-label").string == "Last Competed:"
        assert soup.find(
            id="last_competed-value"
        ).string == self.userdata.last_competed.strftime("%Y/%m/%d")

        # Rating
        assert soup.find(class_="rating-label").string == "Rating"
        assert int(soup.find(class_="rating-text").string) == self.userdata.rating

        default_theme = THEMES["default"]
        styles = serialize_css(soup.find("style", id="main-style").string)

        # Font Family
        font_falmily = get_property_from_css(styles, "#svg-body", "font-family")
        assert font_falmily
        assert font_falmily == default_theme.font_family

        # Background Color
        background_color = get_property_from_css(styles, "#card", "background-color")
        assert background_color
        assert background_color == default_theme.background_color

        # Title Color
        title_color = get_property_from_css(styles, "#title", "color")
        assert title_color
        assert title_color == default_theme.title_color

        # Text Color
        text_color = get_property_from_css(styles, "#svg-body", "color")
        assert text_color
        assert text_color == default_theme.text_color

        # Rating Color
        rating_color = get_property_from_css(styles, ".rating", "color")
        assert rating_color
        assert rating_color == get_rating_color(self.userdata.rating)
        css_text = None
        for rule in styles.cssRules:
            if (
                rule.typeString == "UNKNOWN_RULE"
                and "radial-gradient" in rule.cssText
                and "conic-gradient" in rule.cssText
            ):
                css_text = rule.cssText
                break
        assert css_text
        assert f"radial-gradient({default_theme.background_color}" in css_text
        assert f"conic-gradient({rating_color}" in css_text

    def test_hide_stats(self):
        option = StatsOption()
        option.hide = {"rank", "highest_rating", "rated_matches", "last_competed"}
        stats_card = StatsCard(userdata=self.userdata, option=option)
        soup = BeautifulSoup(stats_card.render(), "html.parser")

        # ID
        assert not soup.find(id="id-label")
        assert not soup.find(id="id-value")
        # Rating
        assert not soup.find(id="rating-label")
        assert not soup.find(id="rating-value")
        # Rank
        assert not soup.find(id="rank-label")
        assert not soup.find(id="rank-value")
        # Highenst Rating
        assert not soup.find(id="highest_rating-label")
        assert not soup.find(id="highest_rating-value")
        # Rated Matches
        assert not soup.find(id="rated_matches-label")
        assert not soup.find(id="rated_matches-value")
        # Last Competed
        assert not soup.find(id="last_competed-label")
        assert not soup.find(id="last_competed-value")

    @pytest.mark.parametrize("width", [100, 400, 1000])
    def test_width_option(self, width):
        option = StatsOption()
        option.width = width
        stats_card = StatsCard(userdata=self.userdata, option=option)
        soup = BeautifulSoup(stats_card.render(), "html.parser")
        svg = soup.find("svg")

        assert "width" in svg.attrs
        assert int(svg.attrs["width"]) == width

    @pytest.mark.parametrize("height", [100, 400, 1000])
    def test_height_option(self, height):
        option = StatsOption()
        option.height = height
        stats_card = StatsCard(userdata=self.userdata, option=option)
        soup = BeautifulSoup(stats_card.render(), "html.parser")
        svg = soup.find("svg")

        assert "height" in svg.attrs
        assert int(svg.attrs["height"]) == height

    def test_theme_option(self):
        option = StatsOption()

        theme = THEMES["darcula"]
        option.theme = theme
        stats_card = StatsCard(userdata=self.userdata, option=option)
        soup = BeautifulSoup(stats_card.render(), "html.parser")

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

        icon_color = get_property_from_css(styles, ".icon", "color")
        assert icon_color
        assert icon_color == theme.icon_color

    @pytest.mark.parametrize(
        "show_history, height",
        [
            (True, "auto"),
            (False, "auto"),
            (0, "auto"),
            (1, "auto"),
            (10, "auto"),
            (True, 500),
            (False, 100),
        ],
    )
    def test_show_history_option(self, show_history, height):
        self._check_competitions_history(show_history=show_history, height=height)

    @pytest.mark.parametrize("show_icons", [None, False, True])
    def test_show_icons_option(self, show_icons: Optional[bool]):
        option = StatsOption()
        if show_icons is not None:
            option.show_icons = show_icons
        stats_card = StatsCard(self.userdata, option=option)
        soup = BeautifulSoup(stats_card.render(), "html.parser")

        icons = soup.find_all(class_="icon")
        assert len(icons) == (4 if show_icons else 0)

        if show_icons:
            for icon_ele, id in zip(
                icons, ["rank", "highest_rating", "rated_matches", "last_competed"]
            ):
                icon_svg = icon_ele.find("svg")
                assert icon_svg.attrs.get("id", "") == id
