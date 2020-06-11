import random
import chess
import time


class Player:
    
    def __init__(self):
        pass


    def random_player(self, board, time_left):
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


    def minimax(self, board: chess.Board, depth: int, player: bool, time_left):
        if time_left() < 10:
            raise Exception("Minimax timed-out. Returning best move from previously completed depth.")

        if depth == -1:
            return self.evaluate(board, player), None

        legal_moves = board.legal_moves
        turn = board.turn

        best_score = float("-inf") if turn == player else float("inf")
        best_move = None

        for move in legal_moves:
            tmp_board = board.copy()
            tmp_board.push(move)
            score, _ = self.minimax(tmp_board, depth - 1, player, time_left)

            if (turn == player): # max
                if score > best_score:
                    best_score = score
                    best_move = move
            else: # min
                if score < best_score:
                    best_score = score
                    best_move = move
        return best_score, best_move

    def minimax_player(self, board, player, time_left):
        best_moves = {}
        depth = 0
        
        while True:
            try:
                best_moves[depth] = self.minimax(board, depth, player, time_left)[1].uci()
                depth += 1
            except Exception:
                return best_moves[depth - 1]

        return best_moves[depth]

