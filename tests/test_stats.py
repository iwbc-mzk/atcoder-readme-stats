import datetime
import cssutils
from cssutils.css import CSSStyleSheet

from bs4 import BeautifulSoup
import pytest

from src.stats import StatsCard, StatsOption
from src.model import UserData
from src.themes import THEMES
from src.utils import get_rating_color


def serialize_css(css: str) -> CSSStyleSheet:
    css = css.replace("\n", "")
    c = []
    q = False
    for s in css:
        if s in ["'", '"']:
            q = not q
        if q or s != " ":
            c.append(s)

    css = "".join(c)
    return cssutils.parseString(css)


class TestStatsCard:
    userdata = UserData(
        id="test_user",
        rank=1000,
        rating=1450,
        highest_rating=400,
        rated_matches=90,
        last_competed=datetime.datetime(2023, 4, 10),
    )

    def _get_property_from_css(self, css, class_or_id, property):
        for rule in css.cssRules:
            if rule.typeString == "STYLE_RULE" and rule.selectorText == class_or_id:
                return rule.style[property]
        return None

    def test_render_with_default_option(self):
        option = StatsOption()
        stats_card = StatsCard(userdata=self.userdata, option=option)
        soup = BeautifulSoup(stats_card.render(), "html.parser")

        svg = soup.find("svg")

        # default width is 450 px
        assert int(svg.attrs["width"]) == 450
        # default height is 200 px
        assert int(svg.attrs["height"]) == 200
        # default viewbox fit width and height
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
        main_styles = serialize_css(soup.find("style", id="main-style").string)

        # Font Family
        font_falmily = self._get_property_from_css(
            main_styles, "#svg-body", "font-family"
        )
        assert font_falmily
        assert font_falmily == default_theme.font_family

        # Background Color
        background_color = self._get_property_from_css(
            main_styles, "#card", "background-color"
        )
        assert background_color
        assert background_color == default_theme.background_color

        # Title Color
        title_color = self._get_property_from_css(main_styles, "#title", "color")
        assert title_color
        assert title_color == default_theme.title_color

        # Text Color
        text_color = self._get_property_from_css(main_styles, "#svg-body", "color")
        assert text_color
        assert text_color == default_theme.text_color

        circle_styles = serialize_css(
            soup.find("style", id="rating-circle-style").string
        )

        # Rating Color
        rating_color = self._get_property_from_css(circle_styles, ".rating", "color")
        assert rating_color
        assert rating_color == get_rating_color(self.userdata.rating)
        css_text = None
        for rule in circle_styles.cssRules:
            if rule.typeString == "UNKNOWN_RULE":
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
        assert int(svg.attrs["width"]) == width

    @pytest.mark.parametrize("height", [100, 400, 1000])
    def test_height_option(self, height):
        option = StatsOption()
        option.height = height
        stats_card = StatsCard(userdata=self.userdata, option=option)
        soup = BeautifulSoup(stats_card.render(), "html.parser")
        svg = soup.find("svg")
        assert int(svg.attrs["height"]) == height

    def test_theme_option(self):
        option = StatsOption()

        theme = THEMES["darcula"]
        option.theme = theme
        stats_card = StatsCard(userdata=self.userdata, option=option)
        soup = BeautifulSoup(stats_card.render(), "html.parser")

        main_styles = serialize_css(soup.find("style", id="main-style").string)

        # Font Family
        font_falmily = self._get_property_from_css(
            main_styles, "#svg-body", "font-family"
        )
        assert font_falmily
        assert font_falmily == theme.font_family

        # Background Color
        background_color = self._get_property_from_css(
            main_styles, "#card", "background-color"
        )
        assert background_color
        assert background_color == theme.background_color

        # Title Color
        title_color = self._get_property_from_css(main_styles, "#title", "color")
        assert title_color
        assert title_color == theme.title_color

        # Text Color
        text_color = self._get_property_from_css(main_styles, "#svg-body", "color")
        assert text_color
        assert text_color == theme.text_color

        circle_styles = serialize_css(
            soup.find("style", id="rating-circle-style").string
        )
