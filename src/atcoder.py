import re
from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

from src.model import UserData


class Atcoder:
    base_url = "https://atcoder.jp/users/"

    def __init__(self, username: str) -> None:
        self._username = username
        self._user_url = urljoin(self.base_url, username)
        self._userdata = UserData(id=self._username)

    def fetch_data(self) -> UserData:
        res = requests.get(self._user_url)
        if res.ok:
            user_soup = BeautifulSoup(res.content, "html.parser")

            self._userdata.rank = self._search_rank(user_soup)
            self._userdata.rating = self._search_rating(user_soup)
            self._userdata.highest_rating = self._search_highest_rating(user_soup)
            self._userdata.rated_matches = self._search_rated_matches(user_soup)
            self._userdata.last_competed = self._search_last_competed(user_soup)

        return self._userdata

    def _search_rank(self, soup: BeautifulSoup) -> int | None:
        rank = None
        rank_label_tag = soup.find("th", string="Rank")
        if rank_label_tag:
            rank_val_tag = rank_label_tag.next_sibling
            if rank_val_tag:
                rank = int(rank_val_tag.text[:-2])

        return rank

    def _search_rating(self, soup: BeautifulSoup) -> int | None:
        rating = None
        rating_label_tag = soup.find("th", string="Rating")
        if rating_label_tag:
            rating_val_tag = rating_label_tag.next_sibling
            if rating_val_tag:
                rating_tag = rating_val_tag.find_all_next("span")
                if rating_tag:
                    rating = int(rating_tag[0].text)

        return rating

    def _search_highest_rating(self, soup: BeautifulSoup) -> int | None:
        highest_rating = None
        highest_rating_label_tag = soup.find("th", string="Highest Rating")
        if highest_rating_label_tag:
            highest_rating_val_tag = highest_rating_label_tag.next_sibling
            if highest_rating_val_tag:
                highest_rating_tags = highest_rating_val_tag.find_all_next("span")
                if highest_rating_tags:
                    highest_rating = int(highest_rating_tags[0].text)

        return highest_rating

    def _search_rated_matches(self, soup: BeautifulSoup) -> int | None:
        rated_matches = 0
        rated_matches_label = soup.find(string="Rated Matches")
        if rated_matches_label:
            rated_matches_label_tag = rated_matches_label.parent
            if rated_matches_label_tag:
                rated_matches_val_tag = rated_matches_label_tag.next_sibling
                if rated_matches_val_tag:
                    rated_matches = int(rated_matches_val_tag.text)

        return rated_matches

    def _search_last_competed(self, soup: BeautifulSoup) -> datetime | None:
        last_competed = None
        last_competed_label_tag = soup.find("th", string="Last Competed")
        if last_competed_label_tag:
            last_competed_val_tag = last_competed_label_tag.next_sibling
            if last_competed_val_tag:
                last_competed = datetime.strptime(
                    last_competed_val_tag.text, "%Y/%m/%d"
                )

        return last_competed
