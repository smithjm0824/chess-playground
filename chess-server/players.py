import random
import chess
import time

class Player:
    def __init__(self):
        pass

    def random_player(self, board):
        legal_moves = board.legal_moves
        random_move = random.choice(list(legal_moves))
        return random_move.uci()

    def evaluate(self, board: chess.Board, player: bool): 
        turn = board.turn
        if board.is_checkmate():
            return -10000 if turn == player else 10000
        if board.is_check():
            return -5000 if turn == player else 5000
        
        material_sum = 0
        weights = {'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 20000}
        for i in range(64):
            piece = board.piece_at(i)
            if piece:
                color_weight = 1 if piece.color == player else -1
                material_sum += weights[piece.symbol().lower()] * color_weight
        return material_sum

    def minimax(self, board: chess.Board, depth: int, start_time: float, player: bool):
        # time_left = (time.time() - start_time) * 1000

        # if time_left < 10:
        #     return None, None

        if depth == 0:
            return self.evaluate(board, player), None

        legal_moves = board.legal_moves
        turn = board.turn

        best_score = float("-inf") if turn == player else float("inf")
        best_move = None

        for move in legal_moves:
            board.push(move)
            score, _ = self.minimax(board, depth - 1, start_time, not player)
            # if score is None:
            #     # return best move from the previous depth
            if (turn == player): # max
                if score > best_score:
                    best_score = score
                    best_move = move
            else: # min
                if score < best_score:
                    best_score = score
                    best_move = move
            board.pop()
        return best_score, best_move

    def minimax_player(self, board, player):
        print("move recorded")
        return self.minimax(board, 3, time.time(), player)[1].uci()