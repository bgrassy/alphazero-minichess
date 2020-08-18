from MiniChessBoard import MiniChessBoard, Bitboard
from Enums import *
import numpy as np
import copy


board = MiniChessBoard()

board.print_board()

# Plays a random game against itself.
moves = board.get_all_moves()
while len(moves) > 0 and not board.is_insufficient_material():
    move = np.random.choice(moves)
    print(move)
    board.make_move(move)
    print(board.in_check(), board.white)
    board.print_board()
    moves = board.get_all_moves()

if board.is_insufficient_material() or not board.in_check():
    print("draw!")
else:
    print("won!")
board.print_board()
