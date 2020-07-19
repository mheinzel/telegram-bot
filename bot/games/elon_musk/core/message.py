from typing import NamedTuple, List
from telegram import Chat, User
import bot.games.elon_musk.core.reply as reply
from bot.games.elon_musk.core.round import Problem, Solution

# I would like to move the 'chat' attribute here, but subclass relationships
# between NamedTuples don't seem to work as expected.
class Message:
    pass

class GameCreated(Message, NamedTuple):
    chat: Chat
    code: str

class GameJoinedPrivate(Message, NamedTuple):
    chat: Chat
    code: str
    joined_user: User

class GameJoined(Message, NamedTuple):
    chat: Chat
    joined_user: User

class GameNotEnoughParticipants(Message, NamedTuple):
    chat: Chat
    code: str
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
    code: str

class RoundNotifyProblem(Message, NamedTuple):
    chat: Chat
    problem: Problem

# Doesn't get the problem.
class RoundNotifyProblemElonMusk(Message, NamedTuple):
    chat: Chat
    giving_problem: User

class RoundDemandSolutions(Message, NamedTuple):
    chat: Chat
    problem: Problem
    solution_order: List[User]
    reply_context: reply.ReplyContext

class RoundSolutionAlreadySubmitted(Message, NamedTuple):
    chat: Chat
    solution: Solution

class RoundNotFinishedYet(Message, NamedTuple):
    chat: Chat
    missing_solutions: List[User]

class RoundSummary(Message, NamedTuple):
    chat: Chat
    problem: Problem
    solutions: List[Solution]

class RoundRevealed(Message, NamedTuple):
    chat: Chat
    code: str
    elon_musk: User
