from telegram import Chat, User
import bot.games.elon_musk.core.message as message
import bot.games.elon_musk.core.reply as reply
from bot.games.elon_musk.core.round import Round, Problem, Solution

def create_game(group_chat, code):
    game = Game(group_chat, code)
    responses = game.init()
    return game, responses

class Game:
    def __init__(self, group_chat: Chat, code: str):
        self.group_chat = group_chat
        self.code = code
        self.participants = []
        self.private_chats = {}
        self.current_round = None
        self.history = []

    def init(self):
        return [message.GameCreated(self.group_chat, self.code)]

    def join_private(self, user: User, private_chat: Chat):
        if user in self.participants:
            return [message.GameJoinedAlready(private_chat, self.code)]

        self.participants.append(user)
        self.private_chats[user.id] = private_chat
        res  = [message.GameJoinedPrivate(private_chat, self.code, user)]
        res += [message.GameJoined(self.group_chat, user)]
        return res

    def start_round(self):
        # One person submits a problem.
        # If only two others submit solutions, they know who the other one is.
        # So we need at least 4 participants.
        if len(self.participants) < 4:
            return [message.GameNotEnoughParticipants(self.group_chat, self.code, self.participants)]

        if self.current_round is not None:
            self.history += [self.current_round]
            # rotate participants, so someone else submits a problem
            self.participants = self.participants[1:] + [self.participants[0]]

        # new round id is larger than all previous ones, starting at 1
        new_round_id = max((r.id for r in self.history), default = 0) + 1
        # first participant submits problem, others submit solutions
        giving_problem = self.participants[0]
        giving_solutions = self.participants[1:]
        new_round = Round(new_round_id, giving_problem, giving_solutions)

        self.current_round = new_round

        # FUTUREWORK: move to Round, but it currently doesn't know about the private_chat
        giving_problem_chat = self.private_chats[giving_problem.id]
        reply_context = reply.SubmitProblem(self.code, new_round.id)
        res  = [message.RoundStarted(self.group_chat, giving_problem, giving_solutions)]
        res += [message.RoundDemandProblem(giving_problem_chat, giving_problem, reply_context)]
        return res

    def submit_problem(self, round_id: int, problem: Problem):
        submitter_chat = self.private_chats[problem.submitted_by.id]

        if round_id != self.current_round.id:
            return [message.RoundProblemNotExpected(submitter_chat, self.code)]
        if problem.submitted_by != self.current_round.giving_problem:
            return [message.RoundProblemNotExpected(submitter_chat, self.code)]

        existing_problem = self.current_round.problem
        if existing_problem is not None:
            # This should only be sent to the person that actually submitted the problem.
            # We don't want to leak the problem to others!
            return [message.RoundProblemAlreadySubmitted(submitter_chat, existing_problem)]

        self.current_round.problem = problem
        giving_solutions = list(self.current_round.missing_solutions())
        elon_musk_chat = self.private_chats[self.current_round.elon_musk.id]

        res  = [message.RoundAcceptProblem(submitter_chat, self.code)]
        reply_context = reply.SubmitSolution(self.code, self.current_round.id)
        res += [message.RoundDemandSolutions(self.group_chat, problem, giving_solutions, reply_context)]
        # Elon Musk doesn't get the problem
        res += [message.RoundNotifyProblemElonMusk(elon_musk_chat, problem.submitted_by)]
        for u in giving_solutions:
            if u != self.current_round.elon_musk:
                private_chat = self.private_chats[u.id]
                res += [message.RoundNotifyProblem(private_chat, problem)]
        return res

    def submit_solution(self, round_id: int, solution: Solution):
        submitter_chat = self.private_chats[solution.submitted_by.id]

        existing_solution = self.current_round.solutions.get(solution.submitted_by)
        if existing_solution is not None:
            return [message.RoundSolutionAlreadySubmitted(self.group_chat, existing_solution)]

        if round_id != self.current_round.id:
            return [message.RoundSolutionNotExpected(submitter_chat, self.code)]
        if self.current_round.problem is None:
            return [message.RoundSolutionNotExpected(submitter_chat, self.code)]
        if solution.submitted_by not in self.current_round.missing_solutions():
            return [message.RoundSolutionNotExpected(submitter_chat, self.code)]

        self.current_round.solutions[solution.submitted_by] = solution

        if len(self.current_round.missing_solutions()) == 0:
            problem = self.current_round.problem
            solutions = list(self.current_round.solutions.values())
            # Group chat, because we assume solutions are submitted there, too.
            return [message.RoundSummary(self.group_chat, problem, solutions)]

        return []

    def reveal(self):
        missing_solutions = list(self.current_round.missing_solutions())
        if len(missing_solutions) > 0:
            return [message.RoundNotFinishedYet(self.group_chat, missing_solutions)]

        elon_musk = self.current_round.elon_musk
        return [message.RoundRevealed(self.group_chat, self.code, elon_musk)]
