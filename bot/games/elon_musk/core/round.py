from typing import NamedTuple, List, Dict
from telegram import User

class Problem(NamedTuple):
    submitted_by: User
    text: str

class Solution(NamedTuple):
    submitted_by: User
    text: str

# There is some redundancy here, with Problem and Solution already containing
# the User that submitted them and then also having the Users as dict keys.
class Round():
    def __init__(self, id: int, giving_problem: User, giving_solutions: List[User]):
        self.id = id
        self.giving_problem = giving_problem
        # no problem or solution was given yet
        self.problem = None
        self.solutions = {u: None for u in giving_solutions}
