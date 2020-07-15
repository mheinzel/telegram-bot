from typing import NamedTuple, List
import bot.games.elon_musk.core.reply as reply
from bot.games.elon_musk.core.shared import Problem, Solution
from telegram import Chat, User

class GameCreated(NamedTuple):
    chat: Chat
    code: str

class GameJoinedPrivate(NamedTuple):
    chat: Chat
    joined_user: User

class GameJoined(NamedTuple):
    chat: Chat
    joined_user: User

class GameNotEnoughParticipants(NamedTuple):
    chat: Chat
    participants: List[User]

class RoundStarted(NamedTuple):
    chat: Chat
    participants: List[User]
    giving_problem: User

class RoundDemandProblem(NamedTuple):
    chat: Chat
    user: User
    reply_context: reply.ReplyContext

class RoundAcceptProblem(NamedTuple):
    chat: Chat

class RoundNotifyProblem(NamedTuple):
    chat: Chat
    problem: Problem

class RoundDemandSolutions(NamedTuple):
    chat: Chat
    problem: Problem
    giving_problem: User
    solution_order: List[User]
    reply_context: reply.ReplyContext

class SolutionAlreadySubmitted(NamedTuple):
    chat: Chat
    solution: Solution

class RoundNotFinishedYet(NamedTuple):
    chat: Chat
    missing_solutions: List[User]

class RoundSummary(NamedTuple):
    chat: Chat
    problem: Problem
    solutions: Solution

class RoundRevealed(NamedTuple):
    chat: Chat
    elon_musk: User
