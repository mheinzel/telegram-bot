from typing import NamedTuple

class ReplyContext:
    pass

class SubmitProblem(ReplyContext, NamedTuple):
    game_code: str
    round: int

class SubmitSolution(ReplyContext, NamedTuple):
    game_code: str
    round: int
