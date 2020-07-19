from typing import NamedTuple, List, Dict
from telegram import User

class Problem(NamedTuple):
    submitted_by: User
    text: str

class Solution(NamedTuple):
    submitted_by: User
    text: str

def create_round(id: int, giving_problem: User, giving_solutions: List[User]):
    # no problem or solution was given yet
    problem = None
    solutions = {u: None for u in giving_solutions}
    return Round(id, giving_problem, problem, solutions)

class Round(NamedTuple):
    id: int
    giving_problem: User
    problem: Problem
    solutions: Dict[User, Solution]
