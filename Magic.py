from MiniChessBoard import Square, Bitboard
import itertools
import pickle
import uuid


FULL_64 = 0xFFFFFFFFFFFFFFFF

# Returns the list of squares that a bishop placed at a given square can
# attack, given the original square and a bitboard of the occupied squares
def bishop_attacks(sq, blocked):
    attacked_squares = []
    sq_rank = sq // 5
    sq_file = sq % 5
    for r, f in zip(range(sq_rank + 1, 5), range(sq_file + 1, 5)):
        attacked_squares.append(5 * r + f)
        if Bitboard.is_set(blocked, 5 * r + f):
            break
    for r, f in zip(range(sq_rank + 1, 5), reversed(range(sq_file))):
        attacked_squares.append(5 * r + f)
        if Bitboard.is_set(blocked, 5 * r + f):
            break
    for r, f in zip(reversed(range(sq_rank)), range(sq_file + 1, 5)):
        attacked_squares.append(5 * r + f)
        if Bitboard.is_set(blocked, 5 * r + f):
            break
    for r, f in zip(reversed(range(sq_rank)), reversed(range(sq_file))):
        attacked_squares.append(5 * r + f)
        if Bitboard.is_set(blocked, 5 * r + f):
            break

    return attacked_squares


# Returns the list of squares that a rook placed at a given square can
# attack, given the original square and a bitboard of the occupied squares
def rook_attacks(sq, blocked):
    attacked_squares = []
    sq_rank = sq // 5
    sq_file = sq % 5
    for f in reversed(range(sq_file)):
        attacked_squares.append(5 * sq_rank + f)
        if Bitboard.is_set(blocked, 5 * sq_rank + f):
            break
    for f in range(sq_file + 1, 5):
        attacked_squares.append(5 * sq_rank + f)
        if Bitboard.is_set(blocked, 5 * sq_rank + f):
            break
    for r in reversed(range(sq_rank)):
        attacked_squares.append(5 * r + sq_file)
        if Bitboard.is_set(blocked, 5 * r + sq_file):
            break
    for r in range(sq_rank + 1, 5):
        attacked_squares.append(5 * r + sq_file)
        if Bitboard.is_set(blocked, 5 * r + sq_file):
            break

    return attacked_squares

# Generates a random 64-bit integer
def gen_64():
    return uuid.uuid4().int >> 64


# Generates a magic number and corresponding table for a given square and piece
# type. Returns a dictionary holding the magic number, table, and the size of
# the bit shift required in the algorithm
def gen_magic(sq, bishop):
    mask = bishop_attacks(sq, 0) if bishop else rook_attacks(sq, 0)

    for bits in range(len(mask), 25):
        for it in range(1000):
            magic = gen_64() & gen_64() & gen_64()
            done = True
            database = {}

            for l in range(len(mask) + 1):
                if not done:
                    break

                blocked_combs = [x for x in itertools.combinations(mask, l)]
                for b in blocked_combs:
                    blocked = Bitboard.gen_bitboard(b)
                    results = Bitboard.gen_bitboard(bishop_attacks(sq, blocked) if bishop else
                                                    rook_attacks(sq, blocked))

                    index = ((blocked * magic) & FULL_64) >> (64 - bits)
                    if index in database and database[index] != results:
                        done = False
                        break

                    database[index] = results
                    Bitboard.print_bitboard(results)
                    print()

            if done:
                return {"mask": Bitboard.gen_bitboard(mask), "magic": magic,
                        "table": database, "bits": bits}

    print("Failed to find magic!")


# Generates all magic numbers and saves them to pickle files
def gen_all_magics():
    bishop_magics = [None] * 25
    rook_magics = [None] * 25 
    for sq in range(25):
        bishop_magics[sq] = gen_magic(sq, True)
        rook_magics[sq] = gen_magic(sq, False)

    with open("bishop_magics.pkl", "wb") as f:
        pickle.dump(bishop_magics, f)
    with open("rook_magics.pkl", "wb") as f:
        pickle.dump(rook_magics, f)

bishop_magics = [None] * 25
for sq in [6]:
    bishop_magics[sq] = gen_magic(sq, True)
