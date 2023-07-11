import re
from datetime import datetime
from urllib.parse import urljoin
from typing import Optional

from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel

from src.model import UserData


class Profile(BaseModel):
    id: str
    rank: Optional[int] = None
    rating: Optional[int] = None
    highest_rating: Optional[int] = None
    rated_matches: Optional[int] = None
    last_competed: Optional[datetime] = None


class Atcoder:
    base_url = "https://atcoder.jp/users/"

    def fetch_userdata(self, username: str) -> UserData:
        userdata = UserData(id=username)

        profile = self.fetch_profile(username)
        self._set_profile(userdata, profile)

        return userdata

    def fetch_profile(self, username: str) -> Profile:
        url = self._get_profile_url(username)
        profile = Profile(id=username)

        res = self._request(url)
        if res.ok:
            soup = BeautifulSoup(res.content, "html.parser")
            profile = Profile(
                **{  # type: ignore
                    "id": username,
                    "rank": self._search_rank(soup),
                    "rating": self._search_rating(soup),
                    "highest_rating": self._search_highest_rating(soup),
                    "rated_matches": self._search_rated_matches(soup),
                    "last_competed": self._search_last_competed(soup),
                }
            )
        else:
            raise ValueError("User Name Not Found.")

        return profile

    def _set_profile(self, userdata: UserData, profile: Profile):
        userdata.rank = profile.rank
        userdata.rating = profile.rating
        userdata.highest_rating = profile.highest_rating
        userdata.rated_matches = profile.rated_matches
        userdata.last_competed = profile.last_competed

    def _get_profile_url(self, username: str) -> str:
        return urljoin(self.base_url, username)

    def _get_competition_history_url(self, username: str) -> str:
        return urljoin(self.base_url, f"{username}/history")

    def _request(self, url: str) -> requests.Response:
        return requests.get(url)

    def _search_rank(self, soup: BeautifulSoup) -> Optional[int]:
        rank = None
        rank_label_tag = soup.find("th", string="Rank")
        if rank_label_tag:
            rank_val_tag = rank_label_tag.next_sibling
            if rank_val_tag:
                rank = int(rank_val_tag.text[:-2])

        return rank

    def _search_rating(self, soup: BeautifulSoup) -> Optional[int]:
        rating = None
        rating_label_tag = soup.find("th", string="Rating")
        if rating_label_tag:
            rating_val_tag = rating_label_tag.next_sibling
            if rating_val_tag:
                rating_tag = rating_val_tag.find_all_next("span")
                if rating_tag:
                    rating = int(rating_tag[0].text)

        return rating

    def _search_highest_rating(self, soup: BeautifulSoup) -> Optional[int]:
        highest_rating = None
        highest_rating_label_tag = soup.find("th", string="Highest Rating")
        if highest_rating_label_tag:
            highest_rating_val_tag = highest_rating_label_tag.next_sibling
            if highest_rating_val_tag:
                highest_rating_tags = highest_rating_val_tag.find_all_next("span")
                if highest_rating_tags:
                    highest_rating = int(highest_rating_tags[0].text)

        return highest_rating

    def _search_rated_matches(self, soup: BeautifulSoup) -> Optional[int]:
        rated_matches = 0
        rated_matches_label = soup.find(string=re.compile("Rated Matches"))
        if rated_matches_label:
            rated_matches_label_tag = rated_matches_label.parent
            if rated_matches_label_tag:
                rated_matches_val_tag = rated_matches_label_tag.next_sibling
                if rated_matches_val_tag:
                    rated_matches = int(rated_matches_val_tag.text)

        return rated_matches

    def _search_last_competed(self, soup: BeautifulSoup) -> Optional[datetime]:
        last_competed = None
        last_competed_label_tag = soup.find("th", string="Last Competed")
        if last_competed_label_tag:
            last_competed_val_tag = last_competed_label_tag.next_sibling
            if last_competed_val_tag:
                last_competed = datetime.strptime(
                    last_competed_val_tag.text, "%Y/%m/%d"
                )

        return last_competed
