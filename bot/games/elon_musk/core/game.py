import bot.games.elon_musk.core.message as message

class Game:
    def __init__(self, chat, code):
        self.chat = chat
        self.code = code
        self.participants = []
        self.current_round = None
        self.history = []

    def init(self):
        created = message.GameCreated(self.chat, self.code)
        return [created]

def create_game(chat, code):
    game = Game(chat, code)
    responses = game.init()
    return game, responses
