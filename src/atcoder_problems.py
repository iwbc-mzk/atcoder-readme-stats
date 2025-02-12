from typing import Optional, List
import json
import datetime
import pickle

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
    execution_time: int | None


class ProblemModel(BaseModel):
    slope: float = 0.0
    intercept: float = 0.0
    variance: float = 0.0
    difficulty: int = 0
    discrimination: float = 0.0
    irt_loglikelihood: float = 0.0
    irt_users: int = 0.0
    is_experimental: bool = False


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
                res.raise_for_status()

        return submissions

    @classmethod
    def fetch_problem_models(cls) -> dict[str, ProblemModel]:
        url = "https://kenkoooo.com/atcoder/resources/problem-models.json"
        res = requests.get(url)
        if res.ok:
            problems: dict = json.loads(res.content)
            problems = {id: ProblemModel(*problem) for id, problem in problems.items()}
            return problems
        else:
            res.raise_for_status()

        return []
