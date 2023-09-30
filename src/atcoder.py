import re
import json
from datetime import datetime
from urllib.parse import urljoin
from typing import Optional, List

from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel


class Profile(BaseModel):
    id: str
    rank: Optional[int] = None
    rating: Optional[int] = None
    highest_rating: Optional[int] = None
    rated_matches: Optional[int] = None
    last_competed: Optional[datetime] = None


class Competition(BaseModel):
    date: datetime
    is_rated: bool
    contest_jp: str
    contest_en: Optional[str]
    rank: Optional[int]
    performance: Optional[int]
    old_rating: Optional[int]
    new_rating: Optional[int]


class UserData(BaseModel):
    id: str
    rank: Optional[int] = None
    rating: Optional[int] = None
    highest_rating: Optional[int] = None
    rated_matches: Optional[int] = None
    last_competed: Optional[datetime] = None
    competitions_history: List[Competition] = []


class Atcoder:
    base_url = "https://atcoder.jp/users/"

    @classmethod
    def fetch_userdata(cls, username: str, need_compe: bool = False) -> UserData:
        userdata = UserData(id=username)

        profile = cls.fetch_profile(username)
        cls._set_profile(userdata, profile)

        if need_compe:
            userdata.competitions_history = cls.fetch_competition_histry(username)

        return userdata

    @classmethod
    def fetch_profile(cls, username: str) -> Profile:
        url = cls._get_profile_url(username)
        profile = Profile(id=username)

        res = cls._request(url)
        if res.ok:
            soup = BeautifulSoup(res.content, "html.parser")
            profile = Profile(
                **{  # type: ignore
                    "id": username,
                    "rank": cls._search_rank(soup),
                    "rating": cls._search_rating(soup),
                    "highest_rating": cls._search_highest_rating(soup),
                    "rated_matches": cls._search_rated_matches(soup),
                    "last_competed": cls._search_last_competed(soup),
                }
            )
        else:
            raise ValueError(
                "User Name Not Found.", "Please make sure username is correct."
            )

        return profile

    @classmethod
    def fetch_competition_histry(cls, username: str) -> List[Competition]:
        url = cls._get_competition_history_url(username)
        histries = []

        res = cls._request(url)
        if res.ok:
            contests = json.loads(res.content)
            for contest in contests:
                competition = Competition(
                    date=datetime.strptime(contest["EndTime"], "%Y-%m-%dT%H:%M:%S%z"),
                    contest_jp=contest["ContestName"],
                    contest_en=contest["ContestNameEn"],
                    is_rated=contest["IsRated"],
                    rank=contest["Place"],
                    performance=contest["Performance"],
                    old_rating=contest["OldRating"],
                    new_rating=contest["NewRating"],
                )
                histries.append(competition)
        else:
            raise ValueError("User Name Not Found.", "")

        return histries

    @classmethod
    def _set_profile(cls, userdata: UserData, profile: Profile):
        userdata.rank = profile.rank
        userdata.rating = profile.rating
        userdata.highest_rating = profile.highest_rating
        userdata.rated_matches = profile.rated_matches
        userdata.last_competed = profile.last_competed

    @classmethod
    def _get_profile_url(cls, username: str) -> str:
        return urljoin(cls.base_url, username)

    @classmethod
    def _get_competition_history_url(cls, username: str) -> str:
        return urljoin(cls.base_url, f"{username}/history/json")

    @classmethod
    def _request(cls, url: str) -> requests.Response:
        return requests.get(url)

    @classmethod
    def _search_rank(cls, soup: BeautifulSoup) -> Optional[int]:
        rank = None
        rank_label_tag = soup.find("th", string="Rank")
        if rank_label_tag:
            rank_val_tag = rank_label_tag.next_sibling
            if rank_val_tag:
                rank = int(rank_val_tag.text[:-2])

        return rank

    @classmethod
    def _search_rating(cls, soup: BeautifulSoup) -> Optional[int]:
        rating = None
        rating_label_tag = soup.find("th", string="Rating")
        if rating_label_tag:
            rating_val_tag = rating_label_tag.next_sibling
            if rating_val_tag:
                rating_tag = rating_val_tag.find_all_next("span")
                if rating_tag:
                    rating = int(rating_tag[0].text)

        return rating

    @classmethod
    def _search_highest_rating(cls, soup: BeautifulSoup) -> Optional[int]:
        highest_rating = None
        highest_rating_label_tag = soup.find("th", string="Highest Rating")
        if highest_rating_label_tag:
            highest_rating_val_tag = highest_rating_label_tag.next_sibling
            if highest_rating_val_tag:
                highest_rating_tags = highest_rating_val_tag.find_all_next("span")
                if highest_rating_tags:
                    highest_rating = int(highest_rating_tags[0].text)

        return highest_rating

    @classmethod
    def _search_rated_matches(cls, soup: BeautifulSoup) -> Optional[int]:
        rated_matches = 0
        rated_matches_label = soup.find(string=re.compile("Rated Matches"))
        if rated_matches_label:
            rated_matches_label_tag = rated_matches_label.parent
            if rated_matches_label_tag:
                rated_matches_val_tag = rated_matches_label_tag.next_sibling
                if rated_matches_val_tag:
                    rated_matches = int(rated_matches_val_tag.text)

        return rated_matches

    @classmethod
    def _search_last_competed(cls, soup: BeautifulSoup) -> Optional[datetime]:
        last_competed = None
        last_competed_label_tag = soup.find("th", string="Last Competed")
        if last_competed_label_tag:
            last_competed_val_tag = last_competed_label_tag.next_sibling
            if last_competed_val_tag:
                last_competed = datetime.strptime(
                    last_competed_val_tag.text, "%Y/%m/%d"
                )

        return last_competed
