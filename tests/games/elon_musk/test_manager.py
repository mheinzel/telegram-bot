from telegram import User, Chat
import bot.games.elon_musk.core.message as msg
import bot.games.elon_musk.core.reply as rpl
from bot.games.elon_musk.core.round import Problem, Solution
from bot.games.elon_musk.manager import Manager

user1 = User(1, "User 1", is_bot = False)
user2 = User(2, "User 2", is_bot = False)
user3 = User(3, "User 3", is_bot = False)
user4 = User(4, "User 4", is_bot = False)
user5 = User(5, "User 5", is_bot = False)

private1 = Chat(11, 'private')
private2 = Chat(12, 'private')
private3 = Chat(13, 'private')
private4 = Chat(14, 'private')
private5 = Chat(15, 'private')

def user_of_chat(chat):
    i = [private1, private2, private3, private4, private5].index(chat)
    return [user1, user2, user3, user4, user5][i]

group1 = Chat(101, 'group')
code1 = "ELON123"

manager = Manager()

# create new game
res = manager.create_game(group_chat = group1)
assert len(res) == 1
assert isinstance(res[0], msg.GameCreated)
assert res[0].chat == group1
code1 = res[0].code

# cannot create another game
res = manager.create_game(group_chat = group1)
assert len(res) == 1
assert isinstance(res[0], msg.GameCreatedAlready)
assert res[0].chat == group1
assert res[0].code == code1

# users cannot join the game from a group chat
res = manager.join_private(code = code1, user = user1, chat = group1)
assert len(res) == 1
assert isinstance(res[0], msg.GameMustBeJoinedFromPrivateChat)
assert res[0].chat == group1
assert res[0].joined_user == user1

# users cannot join a game with non-existing code
res = manager.join_private(code = "ELON007", user = user1, chat = private1)
assert len(res) == 1
assert isinstance(res[0], msg.GameNotFoundByCode)
assert res[0].chat == private1
assert res[0].code == "ELON007"

# users can join the game via private chat
res = manager.join_private(code = code1, user = user1, chat = private1)
res = manager.join_private(code = code1, user = user2, chat = private2)
res = manager.join_private(code = code1, user = user3, chat = private3)
res = manager.join_private(code = code1, user = user4, chat = private4)

# cannot start a non-existing game
res = manager.start_round(chat = Chat(999, 'group'))
assert len(res) == 1
assert isinstance(res[0], msg.GameNotFoundForChat)

# the game can start
res = manager.start_round(chat = group1)
# one person is asked to describe a problem (privately)
assert isinstance(res[1], msg.RoundDemandProblem)
assert isinstance(res[1].reply_context, rpl.SubmitProblem)
ctx_submit_problem1 = res[1].reply_context

# TODO: how to test reply context? put it one layer above, generically?

# that person can submit a problem
problem1 = Problem(user1, "Life is too short.")
res = manager.handle_reply(user1, private1, ctx_submit_problem1, text = "Life is too short.")
assert isinstance(res[0], msg.RoundAcceptProblem)
assert isinstance(res[1], msg.RoundDemandSolutions)
assert isinstance(res[1].reply_context, rpl.SubmitSolution)
ctx_submit_solution1 = res[1].reply_context

# Elon Musk gets asked and submits his solution
assert isinstance(res[2], msg.RoundNotifyProblemElonMusk)
round1_elon = user_of_chat(res[2].chat)
manager.handle_reply(round1_elon, res[1].chat, ctx_submit_solution1, text = "Bad solution.")

# everyone else also gets asked for and submits a solution
assert isinstance(res[3], msg.RoundNotifyProblem)
manager.handle_reply(user_of_chat(res[3].chat), res[3].chat, ctx_submit_solution1, text = "Solution A.")
# the last submitted solution finishes the round
assert isinstance(res[4], msg.RoundNotifyProblem)
res = manager.handle_reply(user_of_chat(res[4].chat), res[4].chat, ctx_submit_solution1, text = "Solution B.")
assert len(res) == 1
assert isinstance(res[0], msg.RoundSummary)

# the round is revealed
res = manager.reveal(group1)
assert len(res) == 1
assert isinstance(res[0], msg.RoundRevealed)
