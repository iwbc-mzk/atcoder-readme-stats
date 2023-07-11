from unittest import mock
import datetime

import pytest
from requests import Response

from src.atcoder import Atcoder


class TestAtcoder:
    _userdata = {
        "id": "iwbc_mzk",
        "rank": 18098,
        "rating": 720,
        "highest_rating": 789,
        "rated_matches": 15,
        "last_competed": datetime.datetime(2023, 7, 2),
    }

    def setup(self):
        self.ac = Atcoder()

    def test_fetch_data_ok(self):
        with open("tests/atcoder.html", "r", encoding="utf-8") as f:
            content = "".join(f.readlines())

            with mock.patch("requests.get") as rget_mock:
                res = Response()
                res.__setattr__("_content", content)
                res.__setattr__("status_code", 200)
                rget_mock.return_value = res
                userdata = self.ac.fetch_userdata("iwbc_mzk")

        userdata_dict = dict(userdata)
        for key in self._userdata:
            assert key in userdata_dict
            assert userdata_dict[key] == self._userdata[key]

    def test_fetch_data_ng(self):
        # Invalid user name
        with mock.patch("requests.get") as rget_mock:
            res = Response()
            res.__setattr__("status_code", 404)
            rget_mock.return_value = res
            with pytest.raises(ValueError) as e:
                self.ac.fetch_userdata("iwbc_mzk")
            assert str(e.value) == "User Name Not Found."

    def test_fetch_profile_ok(self):
        with open("tests/atcoder.html", "r", encoding="utf-8") as f:
            content = "".join(f.readlines())

            with mock.patch("requests.get") as rget_mock:
                res = Response()
                res.__setattr__("_content", content)
                res.__setattr__("status_code", 200)
                rget_mock.return_value = res
                profile = self.ac.fetch_profile("iwbc_mzk")

        profile = dict(profile)
        for key in self._userdata:
            assert key in profile
            assert profile[key] == self._userdata[key]

    def test_fetch_profile_ng(self):
        # Invalid user name
        with mock.patch("requests.get") as rget_mock:
            res = Response()
            res.__setattr__("status_code", 404)
            rget_mock.return_value = res
            with pytest.raises(ValueError) as e:
                self.ac.fetch_profile("iwbc_mzk")
            assert str(e.value) == "User Name Not Found."

