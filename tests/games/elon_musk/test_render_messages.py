import textwrap
from telegram import User, Chat
import bot.games.elon_musk.core.message as msg
import bot.games.elon_musk.core.reply as rpl
from bot.games.elon_musk.core.round import Problem, Solution
from bot.games.elon_musk.manager import Manager

chat = Chat(999, 'private')
user = User(123456789, 'Anne', is_bot = False)
users = [User(1, 'Uno', False), User(2, 'Dos', False), User(3, 'Tres', False)]
problem = Problem(submitted_by = User(9, 'Robin', False), text = "Some tough problem.")
solution = Solution(submitted_by = User(9, 'Oliver', False), text = "A great solution.")
other_solution = Solution(submitted_by = User(9, 'Olivia', False), text = "The best solution.")
solutions = [solution, other_solution]

def test_GameCreated():
    message = msg.GameCreated(chat, code = "CODE")
    expected = textwrap.dedent("""\
            You created a game of Elon Musk in this conversation!
            To join it, start a private conversation with me and run the command "/join CODE"!
    """)
    assert msg.render(message) == expected

def test_GameCreatedAlready():
    message = msg.GameCreatedAlready(chat, code = "CODE")
    expected = textwrap.dedent("""\
            There already is an existing game of Elon Musk in this conversation!
            To join it, start a private conversation with me and run the command "/join CODE"!
    """)
    assert msg.render(message) == expected

def test_GameNotFoundByCode():
    message = msg.GameNotFoundByCode(chat, code = "CODE")
    expected = textwrap.dedent("""\
            The game CODE was not found.
    """)
    assert msg.render(message) == expected

def test_GameNotFoundForChat():
    message = msg.GameNotFoundForChat(chat)
    expected = textwrap.dedent("""\
            There is no game running in this chat. If you want to start one, try "/elonmusk"!
    """)
    assert msg.render(message) == expected

def test_GameMustBeJoinedFromPrivateChat():
    message = msg.GameMustBeJoinedFromPrivateChat(chat, joined_user = user)
    expected = textwrap.dedent("""\
            Hey Anne! You can only join a game from a private chat with me.
    """)
    assert msg.render(message) == expected

def test_GameJoinedAlready():
    message = msg.GameJoinedAlready(chat, code = "CODE")
    expected = textwrap.dedent("""\
            You already joined the game CODE!
    """)
    assert msg.render(message) == expected

def test_GameJoinedPrivate():
    message = msg.GameJoinedPrivate(chat, code = "CODE", joined_user = user)
    expected = textwrap.dedent("""\
            Hey Anne, you joined the game CODE. Welcome to the party!
    """)
    assert msg.render(message) == expected

def test_GameJoined():
    message = msg.GameJoined(chat, joined_user = user)
    expected = textwrap.dedent("""\
            Anne joined the game.
    """)
    assert msg.render(message) == expected

def test_GameNotEnoughParticipants():
    message = msg.GameNotEnoughParticipants(chat, code = "CODE", participants = users)
    expected = textwrap.dedent("""\
            The game CODE does not have enough participants to be started.
            You need at least 4, but only have:
            - Uno
            - Duo
            - Tres

            To join it, start a private conversation with me and run the command "/join CODE"!
    """)
    assert msg.render(message) == expected

def test_RoundStarted():
    message = msg.RoundStarted(chat, giving_problem = user, giving_solutions = users)
    expected = textwrap.dedent("""\
            A new round was started. A problem will be described by Anne and solved by:
            - Uno
            - Dos
            - Tres
    """)
    assert msg.render(message) == expected

def test_RoundDemandProblem():
    message = msg.RoundDemandProblem(chat, user = user, reply_context = None)
    expected = textwrap.dedent("""\
            Hey Anne, please submit your problem by replying to this message!
    """)
    assert msg.render(message) == expected

def test_RoundProblemNotExpected():
    message = msg.RoundProblemNotExpected(chat, code = "CODE")
    expected = textwrap.dedent("""\
            It seems like you tried submitting a problem to the game CODE, but it is not your turn.
    """)
    assert msg.render(message) == expected

def test_RoundProblemAlreadySubmitted():
    message = msg.RoundProblemAlreadySubmitted(chat, problem = problem)
    expected = textwrap.dedent("""\
            You already submitted the following problem to the current round:
            Some tough problem.
    """)
    assert msg.render(message) == expected

def test_RoundAcceptProblem():
    message = msg.RoundAcceptProblem(chat, code = "CODE")
    expected = textwrap.dedent("""\
            Thanks for submitting a problem for the game CODE!
    """)
    assert msg.render(message) == expected

def test_RoundNotifyProblem():
    message = msg.RoundNotifyProblem(chat, problem = problem)
    expected = textwrap.dedent("""\
            The problem is was defined by Robin: Some tough problem.
    """)
    assert msg.render(message) == expected

def test_RoundNotifyProblemElonMusk():
    message = msg.RoundNotifyProblemElonMusk(chat, giving_problem = user)
    expected = textwrap.dedent("""\
            The problem was defined by Anne, but you are Elon Musk.
            This means that you don't get to know the problem, but will still have to propose a solution.
    """)
    assert msg.render(message) == expected

def test_RoundDemandSolutions():
    message = msg.RoundDemandSolutions(chat, solution_order = users, reply_context = None)
    expected = textwrap.dedent("""\
            Each of you received the problem in a private chat with me.
            Please submit your solutions by replying to this message in the following order:
            - Uno
            - Dos
            - Tres
    """)
    assert msg.render(message) == expected

def test_RoundSolutionNotExpected():
    message = msg.RoundSolutionNotExpected(chat, code = "CODE")
    expected = textwrap.dedent("""\
            It seems like you wanted to submit a solution for the game CODE.
            However, I was not expecting that.
    """)
    assert msg.render(message) == expected

def test_RoundSolutionAlreadySubmitted():
    message = msg.RoundSolutionAlreadySubmitted(chat, solution = solution)
    expected = textwrap.dedent("""\
            You already submitted a solution for this problem:
            A great solution.
    """)
    assert msg.render(message) == expected

def test_RoundNotFinishedYet():
    message = msg.RoundNotFinishedYet(chat, missing_solutions = users)
    expected = textwrap.dedent("""\
            The round is not finished yet! Some people have not submitted solutions yet:
            - Uno
            - Dos
            - Tres
    """)
    assert msg.render(message) == expected

def test_RoundSummary():
    message = msg.RoundSummary(chat, solutions = solutions)
    expected = textwrap.dedent("""\
            All solutions have been submitted:
            - Oliver: A great solution.
            - Olivia: The best solution.

            To reveal Elon Musk and the problem, use "/reveal".
    """)
    assert msg.render(message) == expected

def test_RoundRevealed():
    message = msg.RoundRevealed(chat, code = "CODE", problem = problem, elon_musk = user)
    expected = textwrap.dedent("""\
            The problem was: Some tough problem.
            Elon Musk is... Anne!

            You can start a new round by running "/round".
            Before that, new people can still join by sending me "/join CODE" in a private conversation.
    """)
    assert msg.render(message) == expected
