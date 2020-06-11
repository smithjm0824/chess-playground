import chess
from players import Player
import json
import time
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def hello_world():
    game = Game()
    players = Player()
    game.play_game(players.minimax_player, players.random_player)
    return json.dumps(game.history)


class Game:
    def __init__(self):
        self.score = 0
        self.board = chess.Board()
        self.history = {}
        self.id = 0
        self.moves = 0

    def play_game(self, player_1, player_2, time_limit=5000):
        WHITE = chess.WHITE
        init_time = lambda: int(round(time.time() * 1000))

        try:
            while not self.board.is_game_over(claim_draw=True):
                curr_time = init_time()
                time_left = lambda : time_limit - (init_time() - curr_time)

                if self.board.turn == WHITE:
                    move = player_1(self.board, True, time_left)
                else:
                    move = player_2(self.board, time_left)
                self.board.push_uci(move)
                self.publish_board_state()

        except KeyboardInterrupt:
            print("Game interrupted!")

    def publish_board_state(self):
        board_fen = self.board.board_fen()
        self.history[self.moves] = board_fen
        self.moves += 1

#   when game is over, store the game history in redis with the Game id as the key, then increment Game id
#   def cache_results(self):

# TODO: Setup Minimax w/ AlphaBeta Pruning
# TODO: Implement Move Ordering
# TODO: Implement a Book of Opening Moves
# TODO: Implement a Book of EndGame Moves

if __name__ == '__main__':
    app.run()
