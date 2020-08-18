from enum import IntEnum

# Represents the names of a piece
PieceNames = ["p", "n", "b", "r", "q", "k", "-"]

# Represents a square on the board.
Square = IntEnum('Square',
    ["a1", "b1", "c1", "d1", "e1",
    "a2", "b2", "c2", "d2", "e2",
    "a3", "b3", "c3", "d3", "e3",
    "a4", "b4", "c4", "d4", "e4",
    "a5", "b5", "c5", "d5", "e5"], start=0)

# Represents the different colors pieces can have.
Color = IntEnum('Color',  
    ["White", "Black", "NONE"], start=0)

# Represents the different pieces on the board.
Piece = IntEnum('Piece',  
    ["Pawn", "Knight", "Bishop", "Rook", "Queen", "King", "NONE"], start=0)

# Represents the possible categories a given move could fall into
class Flags(IntEnum):
    Quiet = 0,
    Capture = 4,
    KnightProm = 8,
    BishopProm = 9,
    RookProm = 10,
    QueenProm = 11,
    KnightPromCap = 12,
    BishopPromCap = 13,
    RookPromCap = 14,
    QueenPromCap = 15

