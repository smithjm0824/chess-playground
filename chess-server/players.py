import random


def random_player(board):
    legal_moves = board.legal_moves
    random_move = random.choice(list(legal_moves))
    return random_move.uci()
