from unittest import mock
import datetime
from typing import List

import pytest
from requests import Response

from src.atcoder import Atcoder as atcoder, Competition, UserData


class TestAtcoder:
    profile_keys = [
        "id",
        "rank",
        "rating",
        "highest_rating",
        "rated_matches",
        "last_competed",
    ]

    _userdata = UserData(
        **{
            "id": "iwbc_mzk",
            "rank": 18098,
            "rating": 720,
            "highest_rating": 789,
            "rated_matches": 15,
            "last_competed": datetime.datetime(2023, 7, 2),
            "competitions_history": [
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
                        "contest": "Toyota Programming Contest 2023#3（AtCoder Beginner Contest 306）",
                        "rank": 2219,
                        "performance": None,
                        "new_rating": None,
                        "diff": None,
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
                        "contest": "AtCoder Regular Contest 162",
                        "rank": 1253,
                        "performance": 1036,
                        "new_rating": 789,
                        "diff": 38,
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
                        "contest": "Tokio Marine & Nichido Fire Insurance Programming Contest 2023（AtCoder Beginner Contest 307)",
                        "rank": 3814,
                        "performance": 647,
                        "new_rating": 772,
                        "diff": -17,
                    }
                ),
            ],
        }
    )

    def _check_userdata(self, target: UserData, validator: UserData) -> None:
        target, validator = target.model_dump(), validator.model_dump()
        for key in validator:
            assert key in target

            if key == "competitions_history":
                valid_compes = validator.get("competitions_history")
                target_compes = target.get("competitions_history")
                self._check_competition_history(target_compes, valid_compes)
            else:
                assert target[key] == validator[key]

    def _check_competition_history(
        self, target: List[Competition], validator: List[Competition]
    ) -> None:
        assert len(target) == len(validator)

        for val_compe, tar_compe in zip(
            target,
            validator,
        ):
            if isinstance(val_compe, Competition):
                val_compe = val_compe.model_dump()
            if isinstance(tar_compe, Competition):
                tar_compe = tar_compe.model_dump()

            for (v_key, v_val), (t_key, t_val) in zip(
                val_compe.items(), tar_compe.items()
            ):
                assert v_key == t_key
                assert v_val == t_val

    def test_fetch_userdata_ok(self):
        with open("tests/html/profile.html", "r", encoding="utf-8") as pr:
            profile = "".join(pr.readlines())

            with mock.patch("requests.get") as rget_mock:
                pr_res = Response()
                pr_res.__setattr__("_content", profile)
                pr_res.__setattr__("status_code", 200)

                rget_mock.return_value = pr_res
                userdata = atcoder.fetch_userdata("iwbc_mzk")

        valid_userdata = self._userdata.model_copy()
        valid_userdata.competitions_history = []
        self._check_userdata(userdata, valid_userdata)

        # with competitions history
        with open("tests/html/profile.html", "r", encoding="utf-8") as pr, open(
            "tests/html/competition_history.html", "r", encoding="utf-8"
        ) as ch:
            profile = "".join(pr.readlines())
            compe = "".join(ch.readlines())

            with mock.patch("requests.get") as rget_mock:
                pr_res = Response()
                pr_res.__setattr__("_content", profile)
                pr_res.__setattr__("status_code", 200)

                ch_res = Response()
                ch_res.__setattr__("_content", compe)
                ch_res.__setattr__("status_code", 200)

                rget_mock.side_effect = [pr_res, ch_res]
                userdata = atcoder.fetch_userdata("iwbc_mzk", need_compe=True)

        self._check_userdata(userdata, self._userdata)

    def test_fetch_userdata_ng(self):
        # Invalid user name
        with mock.patch("requests.get") as rget_mock:
            res = Response()
            res.__setattr__("status_code", 404)
            rget_mock.return_value = res
            with pytest.raises(ValueError) as e:
                atcoder.fetch_userdata("iwbc_mzk")
            assert e.value.args == ("User Name Not Found.", "Please make sure username is correct.")

    def test_fetch_profile_ok(self):
        with open("tests/html/profile.html", "r", encoding="utf-8") as f:
            content = "".join(f.readlines())

            with mock.patch("requests.get") as rget_mock:
                res = Response()
                res.__setattr__("_content", content)
                res.__setattr__("status_code", 200)
                rget_mock.return_value = res
                profile = atcoder.fetch_profile("iwbc_mzk")

        profile = profile.model_dump()
        userdata = self._userdata.model_dump()
        for key in self.profile_keys:
            assert key in profile
            assert profile[key] == userdata[key]

    def test_fetch_profile_ng(self):
        # Invalid user name
        with mock.patch("requests.get") as rget_mock:
            res = Response()
            res.__setattr__("status_code", 404)
            rget_mock.return_value = res
            with pytest.raises(ValueError) as e:
                atcoder.fetch_profile("iwbc_mzk")
            assert e.value.args == ("User Name Not Found.", "Please make sure username is correct.")

    def test_fetch_competition_history_ok(self):
        with open("tests/html/competition_history.html", "r", encoding="utf-8") as f:
            content = "".join(f.readlines())

            with mock.patch("requests.get") as rget_mock:
                res = Response()
                res.__setattr__("_content", content)
                res.__setattr__("status_code", 200)
                rget_mock.return_value = res
                histories = atcoder.fetch_competition_histry("iwbc_mzk")

        self._check_competition_history(histories, self._userdata.competitions_history)

    def test_fetch_competition_history_ng(self):
        # Invalid user name
        with mock.patch("requests.get") as rget_mock:
            res = Response()
            res.__setattr__("status_code", 404)
            rget_mock.return_value = res
            with pytest.raises(ValueError) as e:
                atcoder.fetch_competition_histry("iwbc_mzk")
            assert e.value.args == ("User Name Not Found.", "")
