from telegram import User
from telegram_bot.bot import BotState
from telegram_bot.games.elon_musk import ElonMuskState
from telegram_bot.message import PrivateWelcome, GroupMissingPrivates
from telegram_bot.games.elon_musk import ElonMuskStarted, ElonMuskYourTurn

user1 = User(1, "User 1", is_bot = False)
user2 = User(2, "User 2", is_bot = False)
user3 = User(3, "User 3", is_bot = False)

private1 = Chat(11, 'private')
private2 = Chat(12, 'private')
private3 = Chat(13, 'private')

group1 = Chat(101, 'group')

bot = BotState()
assert bot.private_chats == {}

# users can start a chat with the bot
res = bot.start_private(user = user1)
assert len(res) == 1
assert res[0] is PrivateWelcome
assert res[0].welcome_user == user1
assert res[0].chat == private1
assert bot.private_chats[user1.id] == private1

# when starting a game, all participants already need to be in a private chat with the bot
game1, res = bot.start_elon_musk(chat = group1, participants = [user1, user2, user3])
assert game1 is Nil
assert len(res) == 1
assert res[0] is GroupMissingPrivates
assert res[0].chat == group1
assert res[0].missing_users == [user2, user3]

# add user2
res = bot.start_private(user = user2)
assert len(res) == 1
assert res[0] is PrivateWelcome
assert res[0].welcome_user == user2
assert res[0].chat == private2
assert bot.private_chats[user1.id] == private2

# add user3
res = bot.start_private(user = user3)
assert len(res) == 1
assert res[0] is PrivateWelcome
assert res[0].welcome_user == user3
assert res[0].chat == private3
assert bot.private_chats[user1.id] == private3

# once they are in private chats, the game can start
game1, res = bot.start_game(chat = group1, participants = [user1, user2, user3])
assert len(res) == 2
# new game is announced
assert res[0] is ElonMuskStarted
assert res[0].chat is group1
assert res[0].participants == [user1, user2, user3]
assert res[0].giving_problem == user1
# one person is asked to describe a problem (privately)
assert res[1] is ElonMuskDemandProblem
assert res[1].chat == private1
assert res[1].user == user1
assert game is ElonMuskState
assert game.participants == [user1, user2, user3]
assert game.private_chats[user1.id] == private1
assert game.private_chats[user2.id] == private2
assert game.private_chats[user3.id] == private3
assert game.giving_problem == user1.id
assert game.solutions == {}


