from typing import NamedTuple, List
import bot.games.elon_musk.core.reply as reply
from bot.games.elon_musk.core.shared import Problem, Solution
from telegram import Chat, User

# I would like to move the 'chat' attribute here, but subclass relationships
# between NamedTuples don't seem to work as expected.
class Message:
    pass

class GameCreated(Message, NamedTuple):
    chat: Chat
    code: str

class GameJoinedPrivate(Message, NamedTuple):
    chat: Chat
    joined_user: User

class GameJoined(Message, NamedTuple):
    chat: Chat
    joined_user: User

class GameNotEnoughParticipants(Message, NamedTuple):
    chat: Chat
    participants: List[User]

class RoundStarted(Message, NamedTuple):
    chat: Chat
    participants: List[User]
    giving_problem: User

class RoundDemandProblem(Message, NamedTuple):
    chat: Chat
    user: User
    reply_context: reply.ReplyContext

class RoundAcceptProblem(Message, NamedTuple):
    chat: Chat

class RoundNotifyProblem(Message, NamedTuple):
    chat: Chat
    problem: Problem

class RoundDemandSolutions(Message, NamedTuple):
    chat: Chat
    problem: Problem
    giving_problem: User
    solution_order: List[User]
    reply_context: reply.ReplyContext

class SolutionAlreadySubmitted(Message, NamedTuple):
    chat: Chat
    solution: Solution

class RoundNotFinishedYet(Message, NamedTuple):
    chat: Chat
    missing_solutions: List[User]

class RoundSummary(Message, NamedTuple):
    chat: Chat
    problem: Problem
    solutions: Solution

class RoundRevealed(Message, NamedTuple):
    chat: Chat
    elon_musk: User
