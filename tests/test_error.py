import datetime
from typing import Union, Literal, Optional

import cssutils
from cssutils.css import CSSStyleSheet
from bs4 import BeautifulSoup
import pytest

from src.cards.error import ErrorCard
from src.atcoder import UserData, Competition
from src.themes import THEMES
from src.utils import get_rating_color
from src.icons import get_icon
from tests.utils import get_property_from_css


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


class TestErrorCard:
    def test_render_error(self):
        MESSAGE = "Main Message"
        SECONDARY_MESSAGE = "Secondary Message"

        error_card = ErrorCard(message=MESSAGE, secondary_message=SECONDARY_MESSAGE)
        soup = BeautifulSoup(error_card.render(), "html.parser")

        svg = soup.find("svg")

        # default width is 600
        assert "width" in svg.attrs
        assert svg.attrs["width"] == "600"

        # default height is not set
        assert "height" in svg.attrs
        assert svg.attrs["height"] == "150"

        # viewbox width and height are 600 and 150
        assert svg.attrs["viewbox"] == "0 0 600 150"

        # default title
        title = soup.find(id="title").string
        assert title == "Something went wrong!"

        # main message
        message = soup.find(id="main-message").string
        assert message == MESSAGE

        # secondary message
        secondary_message = soup.find(id="secondary-message").string
        assert secondary_message == SECONDARY_MESSAGE

        # error card theme is default
        theme = THEMES["default"]

        styles = serialize_css(soup.find("style", id="main-style").string)

        title_color = get_property_from_css(styles, "#title", "color")
        assert title_color == theme.title_color

        main_message_color = get_property_from_css(styles, "#main-message", "color")
        assert main_message_color == theme.text_color

        secondary_message_color = get_property_from_css(
            styles, "#secondary-message", "color"
        )
        assert secondary_message_color == theme.text_color

        font_family = get_property_from_css(styles, "#svg-body", "font-family")
        assert font_family == theme.font_family

        background_color = get_property_from_css(styles, "#card", "background-color")
        assert background_color == theme.background_color

    def test_custom_title(self):
        MESSAGE = "Main Message"
        SECONDARY_MESSAGE = "Secondary Message"
        TITLE = "Custom Title"

        error_card = ErrorCard(
            message=MESSAGE, secondary_message=SECONDARY_MESSAGE, title=TITLE
        )
        soup = BeautifulSoup(error_card.render(), "html.parser")

        svg = soup.find("svg")

        title = svg.find(id="title").string
        assert title == TITLE
