import chess
import players
import json
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def hello_world():
    game = Game()
    game.play_game(players.random_player, players.random_player)
    return json.dumps(game.history)


class Game:
    def __init__(self):
        self.score = 0
        self.board = chess.Board()
        self.history = {}
        self.id = 0
        self.moves = 0

    def play_game(self, player_1, player_2):
        WHITE, BLACK = chess.WHITE, chess.BLACK
        try:
            while not self.board.is_game_over(claim_draw=True):
                if self.board.turn == WHITE:
                    move = player_1(self.board)
                else:
                    move = player_2(self.board)
                self.board.push_uci(move)
                self.publish_board_state()

        except KeyboardInterrupt:
            print("Game interrupted!")

    def publish_board_state(self):
        board_fen = self.board.board_fen()
        self.history[self.moves] = board_fen
        self.moves += 1

    def evaluate(self): 
        material_sum = 0
        weights = {'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 20000}
        for i in range(64):
            piece = self.board.piece_at(i)
            if piece:
                color_weight = 1 if piece.color else -1
                material_sum += weights[piece.symbol().lower()] * color_weight
        return material_sum



#   when game is over, store the game history in redis with the Game id as the key, then increment Game id
#   def cache_results(self):

# TODO: Setup Minimax Vanilla
# TODO: Setup Minimax w/ AlphaBeta Pruning



if __name__ == '__main__':
    app.run()
