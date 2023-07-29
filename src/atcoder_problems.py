from typing import Optional, List
import json
import datetime

import requests

from pydantic import BaseModel


class Submission(BaseModel):
    id: int
    epoch_second: int
    problem_id: str
    contest_id: str
    user_id: str
    language: str
    point: float
    length: int
    result: str
    execution_time: int


class AtcoderProblems:
    @classmethod
    def fetch_submissions(
        cls, user_id: str, from_unix_second: Optional[int] = 0
    ) -> List[Submission]:
        url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={user_id}&from_second={from_unix_second}"

        submissions: List[Submission] = []

        # API側の制限のため500件ずつ取得する
        while True:
            res = requests.get(url)
            if res.ok:
                contents = json.loads(res.content)
                submissions += sorted(
                    [Submission(**v) for v in contents], key=lambda x: x.epoch_second
                )

                if len(contents) < 500:
                    break

                new_from = submissions[-1].epoch_second + 1
                url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={user_id}&from_second={new_from}"
            else:
                break
        return submissions


if __name__ == "__main__":
    AtcoderProblems.fetch_submissions("iwbc_mzk")
