import random
from telegram import Chat, User
import bot.games.elon_musk.core.message as message
import bot.games.elon_musk.core.reply as reply
from bot.games.elon_musk.core.round import Round, Problem, Solution
from bot.games.elon_musk.core.game import create_game, Game

class Manager:
    def __init__(self):
        self.games_by_code = {}
        self.games_by_chat = {}
        self.reply_contexts = {}

    def create_game(self, group_chat: Chat):
        if group_chat in self.games_by_chat:
            return [message.GameCreatedAlready(group_chat, self.games_by_chat[group_chat].code)]

        while True:
            code = "ELON" + str(random.randint(1, max(1000, 10 * len(self.games_by_code))))
            if code not in self.games_by_code:
                break

        game, res = create_game(group_chat, code)
        self.games_by_code[code] = game
        self.games_by_chat[group_chat] = game
        return res

    def join_private(self, code: str, user: User, chat: Chat):
        if chat.type != 'private':
            return [message.GameMustBeJoinedFromPrivateChat(chat, user)]

        game = self.games_by_code.get(code)
        if game is None:
            return [message.GameNotFoundByCode(chat, code)]

        return game.join_private(user, chat)

    def start_round(self, chat: Chat):
        game = self.games_by_chat.get(chat)
        if game is None:
            return [message.GameNotFoundForChat(chat)]

        return game.start_round()

    def handle_reply(self, user: User, chat: Chat, reply_context: reply.ReplyContext, text: str):
        if isinstance(reply_context, reply.SubmitProblem):
            # TODO: handle error case
            game = self.games_by_code[reply_context.game_code]
            problem = Problem(submitted_by = user, text = text)
            return game.submit_problem(reply_context.round, problem)

        if isinstance(reply_context, reply.SubmitSolution):
            # TODO: handle error case
            game = self.games_by_code[reply_context.game_code]
            solution = Solution(submitted_by = user, text = text)
            return game.submit_solution(reply_context.round, solution)

        return []

    def reveal(self, chat: Chat):
        game = self.games_by_chat.get(chat)
        if game is None:
            return [message.GameNotFoundForChat(chat)]

        return game.reveal()
