from random import shuffle

from boardgames.common.models import Board, Result
from .move import Move


class ConnectFourBoard(Board):
    NUM_ROWS = 6
    NUM_COLS = 7

    def __init__(self):
        super().__init__()

        # Board indexed by row, col
        self.grid = [[Tiles.EMPTY for c in range(0, self.NUM_COLS)] for r in range(0, self.NUM_ROWS)]

    def get_tile(self, row, col):
        return self.grid[row][col]

    def undo_move(self, move):
        col = move.dest_col
        row = self.NUM_ROWS - 1
        while self.get_tile(row, col) is Tiles.EMPTY:
            row -= 1
        self.grid[row][col] = Tiles.EMPTY

    def apply_move(self, move):
        dest_row = 0
        while self.get_tile(dest_row, move.dest_col) is not Tiles.EMPTY:
            dest_row += 1
        self.grid[dest_row][move.dest_col] = Tiles.player_to_tile(move.player)

    def print_board(self):
        line = '  ' + ''.join(['-' for _ in range(0, self.NUM_COLS * 2 + 1)])

        col_labels = '   ' + ' '.join([str(x + 1) for x in range(0, self.NUM_COLS)])
        row_labels = ['a', 'b', 'c', 'd', 'e', 'f']
        print(col_labels)
        for inverse_row in range(0, self.NUM_ROWS):
            row = self.NUM_ROWS - 1 - inverse_row
            print(line)
            row_str = str(row_labels[row]) + ' |'
            for col in range(0, self.NUM_COLS):
                row_str += Tiles.tile_to_string(self.get_tile(row, col)) + '|'
            print(row_str)
        print(line)
        print(col_labels)

    def get_winner(self):
        winning_total = 4

        # Rows
        for row in range(0, self.NUM_ROWS):
            for col in range(0, self.NUM_COLS - winning_total + 1):
                val_here = self.get_tile(row, col)
                if val_here != Tiles.EMPTY:
                    match = True
                    for check in range(1, winning_total):
                        if self.get_tile(row, col + check) != val_here:
                            match = False
                            break
                    if match:
                        return Tiles.tile_to_result(val_here)

        # Cols
        for col in range(0, self.NUM_COLS):
            for row in range(0, self.NUM_ROWS - winning_total + 1):
                val_here = self.get_tile(row, col)
                if val_here != Tiles.EMPTY:
                    match = True
                    for check in range(1, winning_total):
                        if self.get_tile(row + check, col) != val_here:
                            match = False
                            break
                    if match:
                        return Tiles.tile_to_result(val_here)

        # Diagonal Up Left
        for row in range(0, self.NUM_ROWS - winning_total + 1):
            for col in range(0, self.NUM_COLS - winning_total + 1):
                val_here = self.get_tile(row, col)
                if val_here != Tiles.EMPTY:
                    match = True
                    for offset in range(1, winning_total):
                        if self.get_tile(row + offset, col + offset) != val_here:
                            match = False
                            break
                    if match:
                        return Tiles.tile_to_result(val_here)

        # Diagonal Up Right
        for row in range(0, self.NUM_ROWS - winning_total + 1):
            for col in range(winning_total - 1, self.NUM_COLS):
                val_here = self.get_tile(row, col)
                if val_here != Tiles.EMPTY:
                    match = True
                    for offset in range(1, winning_total):
                        if self.get_tile(row + offset, col - offset) != val_here:
                            match = False
                            break
                    if match:
                        return Tiles.tile_to_result(val_here)
        # If all else fails
        return Result.NO_WINNER

    def is_terminal(self):
        return self.is_full() or self.get_winner() is not Result.NO_WINNER

    def is_full(self):
        top_row = self.grid[self.NUM_ROWS - 1]
        is_full = True
        for tile in top_row:
            if tile is Tiles.EMPTY:
                is_full = False
                break
        return is_full

    def is_legal_move(self, move):
        return self.get_tile(self.NUM_ROWS - 1, move.dest_col) == Tiles.EMPTY

    def get_legal_moves(self, player):
        moves = []
        for col in range(0, self.NUM_COLS):
            move = Move(col, player)
            if self.is_legal_move(move):
                moves.append(move)
        shuffle(moves)
        return moves


class Tiles:
    EMPTY = 0
    PLAYER_1 = 1
    PLAYER_2 = 2

    TILES_TO_STRING = {
        EMPTY: ' ',
        PLAYER_1: 'o',
        PLAYER_2: 'x',
    }

    PLAYER_NUMBERS_TO_TILE = {
        0: PLAYER_1,
        1: PLAYER_2,
    }

    TILES_TO_RESULT = {
        PLAYER_1: Result.PLAYER_1,
        PLAYER_2: Result.PLAYER_2,
        EMPTY: Result.NO_WINNER,
    }

    @staticmethod
    def tile_to_string(tile):
        return Tiles.TILES_TO_STRING[tile]

    @staticmethod
    def player_to_tile(player):
        return Tiles.PLAYER_NUMBERS_TO_TILE[player.number]

    @staticmethod
    def tile_to_result(tile):
        return Tiles.TILES_TO_RESULT[tile]
