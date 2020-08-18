import pickle
from Enums import *

# Stores utility functions that handle operations on a Bitboard
class Bitboard():
    # Pre-calculated attack bitboards for pieces
    pawn_attacks = [[0x40, 0xa0, 0x140, 0x280, 0x100, 0x800, 0x1400,
                     0x2800, 0x5000, 0x2000, 0x10000, 0x28000,
                     0x50000, 0xa0000, 0x40000, 0x200000, 0x500000,
                     0xa00000, 0x1400000, 0x800000, 0x0, 0x0, 0x0,
                     0x0, 0x0], 
                    [0x0, 0x0, 0x0, 0x0, 0x0, 0x2, 0x5, 0xa, 0x14,
                     0x8, 0x40, 0xa0, 0x140, 0x280, 0x100, 0x800,
                     0x1400, 0x2800, 0x5000, 0x2000, 0x10000, 0x28000,
                     0x50000, 0xa0000, 0x40000]]
    knight_attacks = [0x880, 0x1500, 0x2a20, 0x5040, 0x2080, 0x11004,
                      0x2a008, 0x54411, 0xa0802, 0x41004, 0x220082,
                      0x540105, 0xa8822a, 0x1410054, 0x820088, 0x401040,
                      0x8020a0, 0x1104540, 0x200a80, 0x401100, 0x20800,
                      0x41400, 0x8a800, 0x15000, 0x22000]
    king_attacks = [0x62, 0xe5, 0x1ca, 0x394, 0x308, 0xc43, 0x1ca7,
                    0x394e, 0x729c, 0x6118, 0x18860, 0x394e0, 0x729c0,
                    0xe5380, 0xc2300, 0x310c00, 0x729c00, 0xe53800,
                    0x1ca7000, 0x1846000, 0x218000, 0x538000,
                    0xa70000, 0x14e0000, 0x8c0000]

    # Load magic number information
    with open("bishop_magics.pkl", "rb") as f:
        bishop_magics = pickle.load(f)
    with open("rook_magics.pkl", "rb") as f:
        rook_magics = pickle.load(f)

    full64 = 0xFFFFFFFFFFFFFFFF

    # Constants used for lsb calculation
    debruijn64 = 0x03f79d71b4cb0a89
    index64 = [0, 47,  1, 56, 48, 27,  2, 60,
               57, 49, 41, 37, 28, 16,  3, 61,
               54, 58, 35, 52, 50, 42, 21, 44,
               38, 32, 29, 23, 17, 11,  4, 62,
               46, 55, 26, 59, 40, 36, 15, 53,
               34, 51, 20, 43, 31, 22, 10, 45,
               25, 39, 14, 33, 19, 30,  9, 24,
               13, 18,  8, 12,  7,  6,  5, 63]


    # Gets the bitboard of knight attacks from a given square
    def get_knight_attacks(sq):
        return Bitboard.knight_attacks[sq]


    # Gets the bitboard of bishop attacks from a given square, given the
    # bitboard of occupied pieces.
    def get_bishop_attacks(sq, occupied):
        mask = Bitboard.bishop_magics[sq]["mask"]
        magic = Bitboard.bishop_magics[sq]["magic"]
        bits = Bitboard.bishop_magics[sq]["bits"]
        index = (((occupied & mask) * magic) & Bitboard.full64) >> (64 - bits)

        return Bitboard.bishop_magics[sq]["table"][index]


    # Gets the bitboard of rook attacks from a given square, given the
    # bitboard of occupied pieces.
    def get_rook_attacks(sq, occupied):
        mask = Bitboard.rook_magics[sq]["mask"]
        magic = Bitboard.rook_magics[sq]["magic"]
        bits = Bitboard.rook_magics[sq]["bits"]
        index = (((occupied & mask) * magic) & Bitboard.full64) >> (64 - bits)

        return Bitboard.rook_magics[sq]["table"][index]


    # Gets the bitboard of queen attacks from a given square, given the
    # bitboard of occupied pieces.
    def get_queen_attacks(sq, occupied):
        return Bitboard.get_bishop_attacks(sq, occupied) | Bitboard.get_rook_attacks(sq, occupied)


    # Gets the bitboard of king attacks from a given square.
    def get_king_attacks(sq):
        return Bitboard.king_attacks[sq]


    # Returns whether a given square is occupied on a bitboard
    def is_set(board, square):
        return (board >> square) & 1


    # Sets a square on a bitboard
    def set_square(board, square):
        return board | (1 << square)
        

    # Generates a bitboard from an array of squares
    def gen_bitboard(squares):
        board = 0
        for sq in squares:
            board = Bitboard.set_square(board, sq)

        return board


    # Prints out the bitboard, showing '1' for occupied squares and '0' for
    # unoccupied squares.
    def print_bitboard(board):
        for i in range(4, -1, -1):
            for j in range(5):
                print(Bitboard.is_set(board, 5 * i + j), end="")
            print()


    # Gets the lsb of an integer
    def lsb(b):
        index = ((b ^ (b - 1)) * Bitboard.debruijn64 & Bitboard.full64) >> 58 
        return Bitboard.index64[index]


    # Takes an integer and returns the integer after its least significant bit
    # has been popped.
    def pop_lsb(b):
        return b & (b - 1);

    
    # Returns the number of set bits in an bitboard.
    def popcount(b):
        count = 0
        while b > 0:
            b = b & (b - 1)
            count += 1
        return count


    # Gets the rank of a square on the 5x5 board.
    def get_rank(sq):
        return sq // 5 + 1


    # Gets the file of a square on the 5x5 board.
    def get_file(sq):
        return sq % 5 + 1


    # Returns whether a given square is a valid square on the bitboard.
    def is_valid_square(sq):
        return sq >= 0 and sq < 25

    


