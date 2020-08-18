from Enums import *


# Returns the piece's letter code given a promotion flag
def get_piece(flag):
    if flag == Flags.KnightProm or flag == Flags.KnightPromCap:
        return "N"
    elif flag == Flags.BishopProm or flag == Flags.BishopPromCap:
        return "B"
    elif flag == Flags.RookProm or flag == Flags.RookPromCap:
        return "R"
    elif flag == Flags.QueenProm or flag == Flags.QueenPromCap:
        return "Q"
    else:
        return ""

# Represents a move on a chess board.
class Move:
    def __init__(self, start, end, flags):
        self.start = start
        self.end = end
        self.flags = flags

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_flags(self):
        return self.flags

    def is_capture(self):
        return self.flags & 4

    def is_prom(self):
        return self.flags & 8

    def __str__(self):
        start = Square(self.start).name
        end = Square(self.end).name
        cap = "x" if self.is_capture() else ""
        return start + cap + end + get_piece(self.flags)
