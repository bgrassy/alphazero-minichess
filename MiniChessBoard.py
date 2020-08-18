from Bitboard import Bitboard
from Enums import *
from Move import Move


# Represents a board for Gardner minichess. It stores information about the
# current board state, as well as the move history.
class MiniChessBoard():
    def __init__(self):
        self.board = [None] * 2
        for i in range(2):
            self.board[i] = [0] * 6

        # initialize pieces
        self.board[0][Piece.Pawn] = 0b1111100000
        self.board[0][Piece.Knight] = 0b10
        self.board[0][Piece.Bishop] = 0b100
        self.board[0][Piece.Rook] = 1
        self.board[0][Piece.Queen] = 0b1000
        self.board[0][Piece.King] = 0b10000

        # initialize black pieces
        self.board[1][Piece.Pawn] = self.board[0][Piece.Pawn] << 10
        self.board[1][Piece.Knight] = self.board[0][Piece.Knight] << 20
        self.board[1][Piece.Bishop] = self.board[0][Piece.Bishop] << 20
        self.board[1][Piece.Rook] = self.board[0][Piece.Rook] << 20
        self.board[1][Piece.Queen] = self.board[0][Piece.Queen] << 20
        self.board[1][Piece.King] = self.board[0][Piece.King] << 20

        self.move_count = 0
        self.white = True
        self.moves = [None]
        self.captured = [None]

    
    # Returns the color of the side to move.
    def color_to_move():
        return Color.White if self.white else Color.Black

    # Given a square, returns the color and type of the piece on the square.
    def get_square_info(self, square):
        for c in range(2):
            for p in range(6):
                if Bitboard.is_set(self.board[c][p], square):
                    return Color(c), Piece(p)

        return Color.NONE, Piece.NONE

    
    # Returns the type of piece on a given square.
    def get_square_color(self, square):
        c, p = self.get_square_info(square)
        return c
        

    # Returns the color of a piece on a given square.
    def get_square_piece(self, square):
        c, p = self.get_square_info(square)
        return p

        
    # Prints out the current state of the board.
    def print_board(self):
        for i in range(4, -1, -1):
            for j in range(5):
                sq = 5 * i + j
                c, p = self.get_square_info(sq)
                piece = PieceNames[p] if c == Color.White else PieceNames[p].upper()
                print(piece + " ", end="")
            print()


    # Returns the bitboard of all of the occupied squares on a board
    def get_occupied(self):
        occupied = 0
        for c in range(2):
            for p in range(6):
                occupied |= self.board[c][p]

        return occupied


    # Given a color and piece, returns the bitboard of all pieces on that board
    # with that color and piece.
    def get_pieces(self, color, piece):
        return self.board[color][piece]


    # returns whether the given color attacks the given square
    def attacked(self, color, sq):
        other_color = Color.Black if color == Color.White else Color.White
        pawns = self.get_pieces(color, Piece.Pawn)
        knights = self.get_pieces(color, Piece.Knight)
        bishopQueens = self.get_pieces(color, Piece.Bishop) | self.get_pieces(color, Piece.Queen)
        rookQueens = self.get_pieces(color, Piece.Rook) | self.get_pieces(color, Piece.Queen)
        kings = self.get_pieces(color, Piece.King)

        if pawns & Bitboard.pawn_attacks[other_color][sq]:
            return True
        if knights & Bitboard.get_knight_attacks(sq):
            return True
        if bishopQueens & Bitboard.get_bishop_attacks(sq, self.get_occupied()):
            return True
        if rookQueens & Bitboard.get_rook_attacks(sq, self.get_occupied()):
            return True
        if kings & Bitboard.get_king_attacks(sq):
            return True

        return False


    # Returns whether the current player is in check or not.
    def in_check(self):
        color, other = (Color.White, Color.Black) if self.white else (Color.Black, Color.White)
        sq = Bitboard.lsb(self.get_pieces(color, Piece.King))
        return self.attacked(other, sq)


    # Returns whether the game should be ruled a draw due to insufficient
    # material.
    def is_insufficient_material(self):
        for color in [Color.White, Color.Black]:
            for piece in [Piece.Pawn, Piece.Rook, Piece.Queen]:
                if Bitboard.popcount(self.get_pieces(color, piece)) > 0:
                    return False
            knight_count = Bitboard.popcount(self.get_pieces(color, Piece.Knight))
            bishop_count = Bitboard.popcount(self.get_pieces(color, Piece.Bishop))
            if (bishop_count and knight_count) or bishop_count > 1 or knight_count > 2:
                return False

        return True


    # Given a legal move, applies the move on the chessboard.
    def make_move(self, move):
        start = move.get_start()
        end = move.get_end()
        startBB = 1 << start
        endBB = 1 << end
        flags = move.get_flags()

        start_color, start_piece = self.get_square_info(start)
        end_color, end_piece = self.get_square_info(end)

        self.board[start_color][start_piece] ^= startBB
        self.board[start_color][start_piece] ^= endBB

        if move.is_capture():
            self.board[end_color][end_piece] ^= endBB
            self.captured.append(end_piece)
        else:
            self.captured.append(None)

        if move.is_prom():
            # remove pawn at end place
            self.board[start_color][start_piece] ^= endBB
            if flags == Flags.KnightProm or flags == Flags.KnightPromCap:
                self.board[start_color][Piece.Knight] ^= endBB
            elif flags == Flags.BishopProm or flags == Flags.BishopPromCap:
                self.board[start_color][Piece.Bishop] ^= endBB
            elif flags == Flags.RookProm or flags == Flags.RookPromCap:
                self.board[start_color][Piece.Rook] ^= endBB
            elif flags == Flags.QueenProm or flags == Flags.QueenPromCap:
                self.board[start_color][Piece.Queen] ^= endBB

        self.moves.append(move)
        self.white = not self.white


    # Undoes the last move that was made on the board.
    def unmake_move(self):
        move = self.moves.pop()
        if move is None:
            return

        captured = self.captured.pop()

        start = move.get_start()
        end = move.get_end()
        startBB = 1 << start
        endBB = 1 << end
        flags = move.get_flags()
        start_color, start_piece = self.get_square_info(end)
        other_color = Color.White if start_color == Color.Black else Color.Black

        # replace start piece and remove
        self.board[start_color][start_piece] ^= startBB
        self.board[start_color][start_piece] ^= endBB

        if move.is_capture():
            self.board[other_color][captured] ^= endBB

        if move.is_prom():
            # replace pawn at start
            self.board[start_color][start_piece] ^= startBB
            self.board[start_color][Piece.Pawn] ^= startBB

        self.white = not self.white


    ######################################
    # MOVE GENERATION
    ######################################


    # Gets all the pawn moves (ignoring captures) from a given square.
    def get_pawn_sq_moves(self, sq, color):
        moves = []
        attacks = Bitboard.pawn_attacks[color][sq]
        while attacks:
            end_sq = Bitboard.lsb(attacks)
            # valid capture
            if (abs(Bitboard.get_file(sq) - Bitboard.get_file(end_sq)) == 1
                and self.get_square_piece(end_sq) != Piece.NONE
                and self.get_square_color(end_sq) != color):
                # promotion
                if Bitboard.get_rank(end_sq) == 1 or Bitboard.get_rank(end_sq) == 5:
                    moves.append(Move(sq, end_sq, Flags.KnightPromCap))
                    moves.append(Move(sq, end_sq, Flags.BishopPromCap))
                    moves.append(Move(sq, end_sq, Flags.RookPromCap))
                    moves.append(Move(sq, end_sq, Flags.QueenPromCap))
                else:
                    moves.append(Move(sq, end_sq, Flags.Capture))
            attacks = Bitboard.pop_lsb(attacks)
                    

        end_sq = sq + 5 if color == Color.White else sq - 5
        if (Bitboard.is_valid_square(end_sq) 
            and self.get_square_piece(end_sq) == Piece.NONE):
            if Bitboard.get_rank(end_sq) == 1 or Bitboard.get_rank(end_sq) == 5:
                moves.append(Move(sq, end_sq, Flags.KnightProm))
                moves.append(Move(sq, end_sq, Flags.BishopProm))
                moves.append(Move(sq, end_sq, Flags.RookProm))
                moves.append(Move(sq, end_sq, Flags.QueenProm))
            else:
                moves.append(Move(sq, end_sq, Flags.Quiet))

        return moves


    # Given a starting square and a bitboard of ending squares and a color,
    # returns a list of possible moves.
    def get_piece_moves(self, sq, attacks, color):
        moves = []
        while attacks:
            end_sq = Bitboard.lsb(attacks)
            end_sq_color = self.get_square_color(end_sq)
            if end_sq_color == Color.NONE:
                moves.append(Move(sq, end_sq, Flags.Quiet))
            elif end_sq_color != color:
                moves.append(Move(sq, end_sq, Flags.Capture))
                
            attacks = Bitboard.pop_lsb(attacks)

        return moves


    # Given a color and a piece, returns all moves that pieces of that color
    # can make.
    def get_moves(self, color, piece):
        pieces = self.get_pieces(color, piece)
        moves = []
        while pieces:
            sq = Bitboard.lsb(pieces)
            if piece == Piece.Pawn:
                moves.extend(self.get_pawn_sq_moves(sq, color))
            else:
                if piece == Piece.Knight:
                    attacks = Bitboard.get_knight_attacks(sq)
                elif piece == Piece.Bishop:
                    attacks = Bitboard.get_bishop_attacks(sq, self.get_occupied())
                elif piece == Piece.Rook:
                    attacks = Bitboard.get_rook_attacks(sq, self.get_occupied())
                elif piece == Piece.Queen:
                    attacks = Bitboard.get_queen_attacks(sq, self.get_occupied())
                elif piece == Piece.King:
                    attacks = Bitboard.get_king_attacks(sq)
                moves.extend(self.get_piece_moves(sq, attacks, color))

            pieces = Bitboard.pop_lsb(pieces)

        return moves


    # Returns whether a given pseudo-legal move is legal on the board or not.
    def is_legal(self, move):
        legal = True
        self.make_move(move)
        self.white = not self.white
        if self.in_check():
            legal = False
        self.white = not self.white
        self.unmake_move()

        return legal


    # Returns the list of all legal moves in a position.
    def get_all_moves(self):
        color = Color.White if self.white else Color.Black
        moves = self.get_moves(color, Piece.Pawn)
        moves.extend(self.get_moves(color, Piece.Knight))
        moves.extend(self.get_moves(color, Piece.Bishop))
        moves.extend(self.get_moves(color, Piece.Rook))
        moves.extend(self.get_moves(color, Piece.Queen))
        moves.extend(self.get_moves(color, Piece.King))

        return [move for move in moves if self.is_legal(move)]
