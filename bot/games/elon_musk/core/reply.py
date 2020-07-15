from typing import NamedTuple

class ReplyContext:
    pass

class SubmitProblem(ReplyContext, NamedTuple):
    round: int

class SubmitSolution(ReplyContext, NamedTuple):
    round: int
