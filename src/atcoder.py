import re
from datetime import datetime
from urllib.parse import urljoin
from typing import Optional

from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel


class UserData(BaseModel):
    id: str
    rank: int = 0
    rating: int = 0
    highest_rating: int = 0
    rated_matches: int = 0
    last_competed: Optional[datetime] = None


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

    def _search_rank(self, soup: BeautifulSoup) -> int:
        rank_title = soup.find(string="Rank").parent
        rank = int(rank_title.next_sibling.string[:-2])

        return rank

    def _search_rating(self, soup: BeautifulSoup) -> int:
        rating_title = soup.find(string="Rating").parent
        rating_value = rating_title.next_sibling
        rating = int(rating_value.find_all("span")[0].string)

        return rating

    def _search_highest_rating(self, soup: BeautifulSoup) -> int:
        highest_rating_title = soup.find(string="Highest Rating").parent
        highest_rating_value = highest_rating_title.next_sibling
        highest_rating = int(highest_rating_value.find_all("span")[0].string)

        return highest_rating

    def _search_rated_matches(self, soup: BeautifulSoup) -> int:
        rated_matches_title = soup.find(string=re.compile("Rated Matches")).parent
        rated_matches = int(rated_matches_title.next_sibling.string)

        return rated_matches

    def _search_last_competed(self, soup: BeautifulSoup) -> datetime:
        last_competed_title = soup.find(string="Last Competed").parent
        last_competed_value = last_competed_title.next_sibling.string
        last_competed = datetime.strptime(last_competed_value, "%Y/%m/%d")

        return last_competed
