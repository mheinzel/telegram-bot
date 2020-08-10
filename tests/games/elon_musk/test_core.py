from telegram import User, Chat
import bot.games.elon_musk.core.message as msg
import bot.games.elon_musk.core.reply as rpl
from bot.games.elon_musk.core.round import Problem, Solution
from bot.games.elon_musk.core.game import Game, create_game

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

group1 = Chat(101, 'group')
code1 = "ELON123"

# create new game
game1, res = create_game(group_chat = group1, code = code1)
assert len(res) == 1
assert isinstance(res[0], msg.GameCreated)
assert res[0].chat == group1
assert res[0].code == code1

# users can join the game via private chat
# user1
res = game1.join_private(user = user1, private_chat = private1)
assert len(res) == 2
assert isinstance(res[0], msg.GameJoinedPrivate)
assert res[0].chat == private1
assert res[0].joined_user == user1
assert isinstance(res[1], msg.GameJoined)
assert res[1].chat == group1
assert res[1].joined_user == user1
# user2
res = game1.join_private(user = user2, private_chat = private2)
assert len(res) == 2
assert isinstance(res[0], msg.GameJoinedPrivate)
assert res[0].chat == private2
assert res[0].joined_user == user2
assert isinstance(res[1], msg.GameJoined)
assert res[1].chat == group1
assert res[1].joined_user == user2
# user3
res = game1.join_private(user = user3, private_chat = private3)
assert len(res) == 2
assert isinstance(res[0], msg.GameJoinedPrivate)
assert res[0].chat == private3
assert res[0].joined_user == user3
assert isinstance(res[1], msg.GameJoined)
assert res[1].chat == group1
assert res[1].joined_user == user3

# users can only join once
res = game1.join_private(user = user2, private_chat = private2)
assert len(res) == 1
assert isinstance(res[0], msg.GameJoinedAlready)
assert res[0].chat == private2
assert res[0].code == code1

# at least 4 participants are needed to start a game
res = game1.start_round()
assert len(res) == 1
assert isinstance(res[0], msg.GameNotEnoughParticipants)
assert res[0].chat == group1
assert res[0].participants == [user1, user2, user3]
assert game1.current_round is None

# user4
res = game1.join_private(user = user4, private_chat = private4)
assert len(res) == 2
assert isinstance(res[0], msg.GameJoinedPrivate)
assert res[0].chat == private4
assert res[0].joined_user == user4
assert isinstance(res[1], msg.GameJoined)
assert res[1].chat == group1
assert res[1].joined_user == user4

# now the game can start
res = game1.start_round()
assert len(res) == 2
# new game is announced
assert isinstance(res[0], msg.RoundStarted)
assert res[0].chat == group1
assert res[0].giving_problem == user1
assert res[0].giving_solutions == [user2, user3, user4]
# one person is asked to describe a problem (privately)
assert isinstance(res[1], msg.RoundDemandProblem)
assert res[1].chat == private1
assert res[1].user == user1
assert isinstance(res[1].reply_context, rpl.SubmitProblem)
round1 = res[1].reply_context.round

# solutions can't be submitted yet
res = game1.submit_solution(round1, Solution(user3, "blabla"))
assert len(res) == 1
assert isinstance(res[0], msg.RoundSolutionNotExpected)
assert res[0].chat == private3
assert res[0].code == code1

# most participants can't submit a problem
res = game1.submit_problem(round1, Problem(user2, "I can't submit a problem."))
assert len(res) == 1
assert isinstance(res[0], msg.RoundProblemNotExpected)
assert res[0].chat == private2
assert res[0].code == code1

# but one person can submit a problem
problem1 = Problem(user1, "Life is too short.")
res = game1.submit_problem(round1, problem1)
assert len(res) == 5
# acknowledge
assert isinstance(res[0], msg.RoundAcceptProblem)
assert res[0].chat == private1
# update the group chat
assert isinstance(res[1], msg.RoundDemandSolutions)
assert res[1].chat == group1
assert res[1].problem == problem1
assert res[1].solution_order == [user2, user3, user4]
assert isinstance(res[1].reply_context, rpl.SubmitSolution)
assert res[1].reply_context.round == round1
# tell every user the problem (first one is the randomly chosen "Elon Musk")
assert isinstance(res[2], msg.RoundNotifyProblemElonMusk) # doesn't contain problem
assert isinstance(res[3], msg.RoundNotifyProblem)
assert res[3].problem == problem1
assert isinstance(res[4], msg.RoundNotifyProblem)
assert res[4].problem == problem1
assert set(r.chat for r in res[2:5]) == {private2, private3, private4}
round1_elon = [user2, user3, user4][[private2, private3, private4].index(res[2].chat)]

# problem can't be changed afterwards
res = game1.submit_problem(round1, Problem(user1, "Life is too long."))
assert len(res) == 1
# acknowledge
assert isinstance(res[0], msg.RoundProblemAlreadySubmitted)
assert res[0].chat == private1
assert res[0].problem == problem1

# other participants submit their solutions in order
solution_user1 = Solution(user1, "Solution 1")
solution_user2 = Solution(user2, "Solution 2")
solution_user3 = Solution(user3, "Solution 3")
solution_user4 = Solution(user4, "Solution 4")
solution_user5 = Solution(user5, "Solution 5")
res = game1.submit_solution(round1, solution_user2)
# we don't want the noise of acknowledging every solution in the group chat.
# if unsure, participants can try revealing the round.
assert len(res) == 0
res = game1.submit_solution(round1, solution_user3)
assert len(res) == 0

# solutions can only be submitted once
res = game1.submit_solution(round1, solution_user2)
assert len(res) == 1
assert isinstance(res[0], msg.RoundSolutionAlreadySubmitted)
assert res[0].chat == group1
assert res[0].solution == solution_user2

# can't submit both problem and solution
res = game1.submit_solution(round1, solution_user1)
assert len(res) == 1
assert isinstance(res[0], msg.RoundSolutionNotExpected)
assert res[0].chat == private1
assert res[0].code == code1

# user5 joins while the round is still running
res = game1.join_private(user = user5, private_chat = private5)
assert len(res) == 2
assert isinstance(res[0], msg.GameJoinedPrivate)
assert res[0].chat == private5
assert res[0].joined_user == user5
assert isinstance(res[1], msg.GameJoined)
assert res[1].chat == group1
assert res[1].joined_user == user5

# can't submit solution if not part of the round
res = game1.submit_solution(round1, solution_user5)
assert len(res) == 1
assert isinstance(res[0], msg.RoundSolutionNotExpected)
assert res[0].chat == private5
assert res[0].code == code1

# user4 is still missing, so we can't reveal
res = game1.reveal()
assert len(res) == 1
assert isinstance(res[0], msg.RoundNotFinishedYet)
assert res[0].chat == group1
assert res[0].missing_solutions == [user4]

# user4 submits solution
res = game1.submit_solution(round1, solution_user4)
assert len(res) == 1
assert isinstance(res[0], msg.RoundSummary)
assert res[0].chat == group1
assert res[0].problem == problem1
assert len(res[0].solutions) == 3
assert res[0].solutions[0] == solution_user2
assert res[0].solutions[1] == solution_user3
assert res[0].solutions[2] == solution_user4

# the round is revealed
res = game1.reveal()
assert len(res) == 1
assert isinstance(res[0], msg.RoundRevealed)
assert res[0].chat == group1
assert res[0].elon_musk == round1_elon

# start another round
res = game1.start_round()
assert len(res) == 2
# new game is announced
assert isinstance(res[0], msg.RoundStarted)
assert res[0].chat == group1
assert res[0].giving_problem == user2
assert res[0].giving_solutions == [user3, user4, user5, user1]
# next person is asked to describe a problem (privately)
assert isinstance(res[1], msg.RoundDemandProblem)
assert res[1].chat == private2
assert res[1].user == user2
assert isinstance(res[1].reply_context, rpl.SubmitProblem)
round2 = res[1].reply_context.round
