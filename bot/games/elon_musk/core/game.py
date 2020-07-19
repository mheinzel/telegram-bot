import bot.games.elon_musk.core.message as message
import bot.games.elon_musk.core.reply as reply

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
        self.participants += [user]
        self.private_chats[user.id] = chat
        res  = [message.GameJoinedPrivate(chat, self.code, user)]
        res += [message.GameJoined(self.chat, user)]
        return res
