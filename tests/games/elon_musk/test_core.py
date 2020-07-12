from telegram import User, Chat
from bot.games.elon_musk.core.game import Game
from bot.games.elon_musk.core.shared import Problem, Solution
import bot.games.elon_musk.core.message as msg
import bot.games.elon_musk.core.context as ctx

user1 = User(1, "User 1", is_bot = False)
user2 = User(2, "User 2", is_bot = False)
user3 = User(3, "User 3", is_bot = False)
user4 = User(3, "User 3", is_bot = False)

private1 = Chat(11, 'private')
private2 = Chat(12, 'private')
private3 = Chat(13, 'private')
private4 = Chat(13, 'private')

group1 = Chat(101, 'group')

# create new game
game1, res = Game(chat = group1, code = "ELON123")
assert len(res) == 1
assert res[0] is msg.GameCreated
assert res[0].chat == group1
assert res[0].code == "ELON123"
assert game1.participants == []
assert game1.current_round is Nil
assert game1.history == []

# users can join the game via private chat
# user1
res = game1.join_private(user = user1, chat = private1)
assert len(res) == 2
assert res[0] is msg.GameJoinedPrivate
assert res[0].chat == private1
assert res[0].joined_user == user1
assert res[1] is msg.GameJoined
assert res[1].chat == group1
assert res[1].joined_user == user1
# user2
res = game1.join_private(user = user2, chat = private2)
assert len(res) == 2
assert res[0] is msg.GameJoinedPrivate
assert res[0].chat == private2
assert res[0].joined_user == user2
assert res[1] is msg.GameJoined
assert res[1].chat == group1
assert res[1].joined_user == user2
# user3
res = game1.join_private(user = user3, chat = private3)
assert len(res) == 2
assert res[0] is msg.GameJoinedPrivate
assert res[0].chat == private3
assert res[0].joined_user == user3
assert res[1] is msg.GameJoined
assert res[1].chat == group1
assert res[1].joined_user == user3
# some checks
assert game1.participants == [user1, user2, user3]
assert game1.private_chats[user1.id] == private1
assert game1.private_chats[user2.id] == private2
assert game1.private_chats[user3.id] == private3

# at least 4 participants are needed to start a game
res = game1.start_round()
assert len(res) == 1
assert res[0] is msg.GameNotEnoughParticipants
assert res[0].chat == group1
assert res[0].participants == [user1, user2, user3]
assert game1.current_round is Nil

# user4
res = game1.join_private(user = user3, chat = private3)
assert len(res) == 2
assert res[0] is msg.GameJoinedPrivate
assert res[0].chat == private3
assert res[0].joined_user == user3
assert res[1] is msg.GameJoined
assert res[1].chat == group1
assert res[1].joined_user == user3

# now the game can start
res = game1.start_round()
assert len(res) == 2
# new game is announced
assert res[0] is msg.RoundStarted
assert res[0].chat == group1
assert res[0].participants == [user1, user2, user3, user4]
assert res[0].giving_problem == user1
# one person is asked to describe a problem (privately)
assert res[1] is msg.RoundDemandProblem
assert res[1].chat == private1
assert res[1].user == user1
assert res[1].register_message_context is ctx.SubmitProblem
round1 = res[1].register_message_context.round
assert game1.current_round.id == round1
assert game1.current_round.giving_problem == user1.id
assert game1.current_round.solutions == {}

# this person can submit a problem
problem1 = Problem(user1, "Life is too short.")
res = game1.submit_problem(round1, problem1)
assert len(res) == 2
# acknowledge
assert res[0] is msg.RoundAcceptProblem
assert res[0].chat == private1
# update the group chat
assert res[1] is msg.RoundDemandSolutions
assert res[1].chat == group1
assert res[1].problem == problem1
assert res[1].giving_problem == user1
assert res[1].solution_order == [user2, user3, user4]
assert res[1].register_message_context is ctx.SubmitSolution
assert res[1].register_message_context.round == round1
# tell every user the problem (first one is the randomly chosen "Elon Musk")
assert res[2] is msg.RoundNotifyProblem
assert res[2].problem == Problem(user1, "Elon Musk")
assert res[3] is msg.RoundNotifyProblem
assert res[3].problem == problem1
assert res[4] is msg.RoundNotifyProblem
assert res[4].problem == problem1
assert set(r.chat for r in res[2:4]) == {private2, private3, private4}
round1_elon = res[2].user

# other participants submit their solutions in order
# TODO should methods take users or IDs?
solution_user2 = Solution(user2, "Solution 2")
solution_user3 = Solution(user3, "Solution 3")
solution_user4 = Solution(user4, "Solution 4")
res = game1.submit_solution(round1, solution_user2)
assert len(res) == 0 # TODO any further updates here?
res = game1.submit_solution(round1, solution_user3)
assert len(res) == 0 # TODO any further updates here?

# solutions can only be submitted once
res = game1.submit_solution(round1, solution_user2)
assert len(res) == 1
assert res[0] is msg.SolutionAlreadySubmitted
assert res[0].chat == group1
assert res[0].solution == solution_user2

# user4 is still missing, so we can't reveal
res = game1.reveal()
assert len(res) == 1
assert res[0] is msg.RoundNotFinishedYet
assert res[0].chat == group1
assert res[0].missing_solutions == [user4]

# user4 submits solution
res = game1.submit_solution(round1, solution_user4)
assert len(res) == 1
assert res[0] is msg.RoundSummary
assert res[0].chat == group1
assert res[0].problem == problem1
assert len(res[0].solutions) == 3
assert res[0].solutions[0] == solution_user2
assert res[0].solutions[1] == solution_user3
assert res[0].solutions[2] == solution_user4

# the game is revealed
res = game1.reveal()
assert len(res) == 1
assert res[0] is msg.RoundRevealed
assert res[0].chat == group1
assert res[0].elon_musk == round1_elon


# start another round
res = game1.start_round()
assert len(res) == 2
# new game is announced
assert res[0] is msg.RoundStarted
assert res[0].chat == group1
assert res[0].participants == [user1, user2, user3, user4, user5]
assert res[0].giving_problem == user2
# one person is asked to describe a problem (privately)
assert res[1] is msg.RoundDemandProblem
assert res[1].chat == private2
assert res[1].user == user2
assert res[1].register_message_context is ctx.SubmitProblem
round2 = res[1].register_message_context.round
assert game1.current_round.id == round2
assert game1.current_round.giving_problem == user2.id
assert game1.current_round.solutions == {}
assert len(game1.history) == 1
assert game1.history[0].id == round1
