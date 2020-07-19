import bot.games.elon_musk.core.message as message
import bot.games.elon_musk.core.reply as reply
from bot.games.elon_musk.core.round import Round, Problem, Solution

def create_game(chat, code):
    game = Game(chat, code)
    responses = game.init()
    return game, responses

class Game:
    def __init__(self, chat, code):
        self.chat = chat
        self.code = code
        self.participants = []
        self.private_chats = {}
        self.current_round = None
        self.history = []

    def init(self):
        return [message.GameCreated(self.chat, self.code)]

    def join_private(self, user, chat):
        if user in self.participants:
            # TODO: add helpful message
            return []

        self.participants.append(user)
        self.private_chats[user.id] = chat
        res  = [message.GameJoinedPrivate(chat, self.code, user)]
        res += [message.GameJoined(self.chat, user)]
        return res

    def start_round(self):
        # One person submits a problem.
        # If only two others submit solutions, they know who the other one is.
        # So we need at least 4 participants.
        if len(self.participants) < 4:
            return [message.GameNotEnoughParticipants( self.chat, self.code, self.participants)]

        if self.current_round is not None:
            self.history += [self.current_round]
        giving_problem = self.participants[0]
        giving_solutions = self.participants[1:]
        # new round id is larger than all previous ones, starting at 1
        new_round_id = max((r.id for r in self.history), default = 0) + 1
        new_round = Round(new_round_id, giving_problem, giving_solutions)
        self.current_round = new_round
        giving_problem_chat = self.private_chats[giving_problem.id]
        reply_context = reply.SubmitProblem(new_round.id)
        res  = [message.RoundStarted(self.chat, self.participants, giving_problem)]
        res += [message.RoundDemandProblem(giving_problem_chat, giving_problem, reply_context)]
        return res

    # Currently (deliberately) doesn't check who submitted the solution.
    # Maybe this allows things like forwarding problems to other users and
    # letting them submit a solution by replying to the message?
    def submit_problem(self, round_id, problem):
        if round_id != self.current_round.id:
            # TODO: add helpful message
            return []
        if self.current_round.problem is not None:
            # TODO: add helpful message
            return []

        self.current_round.problem = problem
        # We could also use `problem.submitted_by` here, but at noted above,
        # we don't check who that is, so we might not have their private chat.
        giving_problem = self.current_round.giving_problem
        giving_solutions = list(self.current_round.solutions.keys())
        elon_musk = giving_solutions[0] # TODO: pick randomly
        def message_notify(user, their_problem):
            chat = self.private_chats[user.id]
            return message.RoundNotifyProblem(chat, giving_problem, their_problem)
        res  = [message.RoundAcceptProblem(self.private_chats[giving_problem.id], self.code)]
        res += [message_notify(elon_musk, None)] # doesn't get problem
        for u in giving_solutions:
            if u != elon_musk:
                res += [message_notify(u, problem)]
        return giving_solutions
        return res
