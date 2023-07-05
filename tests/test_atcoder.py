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

    def test_fetch_data_ok(self):
        ac = Atcoder("iwbc_mzk")

        with open("tests/atcoder.html", "r", encoding="utf-8") as f:
            content = "".join(f.readlines())

            with mock.patch("requests.get") as rget_mock:
                res = Response()
                res.__setattr__("_content", content)
                res.__setattr__("status_code", 200)
                rget_mock.return_value = res
                userdata = ac.fetch_data()

        userdata_dict = dict(userdata)
        for key in self._userdata:
            assert key in userdata_dict
            assert userdata_dict[key] == self._userdata[key]

    def test_fetch_data_ng(self):
        ac = Atcoder("iwbc_mzk")

        # Invalid user name
        with mock.patch("requests.get") as rget_mock:
            res = Response()
            res.__setattr__("status_code", 404)
            rget_mock.return_value = res
            with pytest.raises(ValueError) as e:
                ac.fetch_data()
            assert str(e.value) == "User Name Not Found."
