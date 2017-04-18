from math import inf

from boardgames.common.models import AIPlayer, HumanPlayer, Result
from .board import Tiles


class HumanConnectFourPlayer(HumanPlayer):
    pass


class AIConnectFourPlayer(AIPlayer):

    def get_weights_for_sets(self):
        return [
            0,
            0.1,
            2,
            6,
            inf
        ]

    def get_value_for_board(self, board, player):
        winner = board.get_winner()
        if Result.result_to_player_number(winner) == player.number:
            return self.winning_move_score
        elif winner == Result.NO_WINNER:
            return self.get_value_for_non_winning_board(board, player)
        else:
            return -1 * self.winning_move_score

    def get_value_for_non_winning_board(self, board, player):
        value = 0
        weights = self.get_weights_for_sets()
        winning_total = 4

        # Rows
        for row in range(0, board.NUM_ROWS):
            for col in range(0, board.NUM_COLS - winning_total + 1):
                open_row = True
                active_tile = board.get_tile(row, col)
                count = 0
                for check in range(1, winning_total):
                    this_tile = board.get_tile(row, col + check)
                    if active_tile == Tiles.EMPTY and this_tile != Tiles.EMPTY:
                        active_tile = this_tile
                    if this_tile == active_tile:
                        count += 1
                    elif this_tile != Tiles.EMPTY:
                        open_row = False
                        break

                if open_row:
                    value += (1 if Tiles.player_to_tile(player) == active_tile else -1) * weights[count]

        # Cols
        for col in range(0, board.NUM_COLS):
            for row in range(0, board.NUM_ROWS - winning_total + 1):
                open_row = True
                active_tile = board.get_tile(row, col)
                count = 0
                for check in range(1, winning_total):
                    this_tile = board.get_tile(row + check, col)
                    if active_tile == Tiles.EMPTY and this_tile != Tiles.EMPTY:
                        active_tile = this_tile
                    if this_tile == active_tile:
                        count += 1
                    elif this_tile != Tiles.EMPTY:
                        open_row = False
                        break

                if open_row:
                    value += (1 if Tiles.player_to_tile(player) == active_tile else -1) * weights[count]

        # Diagonal Up Left
        for row in range(0, board.NUM_ROWS - winning_total + 1):
            for col in range(0, board.NUM_COLS - winning_total + 1):
                open_row = True
                active_tile = board.get_tile(row, col)
                count = 0
                for check in range(1, winning_total):
                    this_tile = board.get_tile(row + check, col + check)
                    if active_tile == Tiles.EMPTY and this_tile != Tiles.EMPTY:
                        active_tile = this_tile
                    if this_tile == active_tile:
                        count += 1
                    elif this_tile != Tiles.EMPTY:
                        open_row = False
                        break

                if open_row:
                    value += (1 if Tiles.player_to_tile(player) == active_tile else -1) * weights[count]

        # Diagonal Up Right
        for row in range(0, board.NUM_ROWS - winning_total + 1):
            for col in range(winning_total - 1, board.NUM_COLS):
                open_row = True
                active_tile = board.get_tile(row, col)
                count = 0
                for check in range(1, winning_total):
                    this_tile = board.get_tile(row + check, col - check)
                    if active_tile == Tiles.EMPTY and this_tile != Tiles.EMPTY:
                        active_tile = this_tile
                    if this_tile == active_tile:
                        count += 1
                    elif this_tile != Tiles.EMPTY:
                        open_row = False
                        break

                if open_row:
                    value += (1 if Tiles.player_to_tile(player) == active_tile else -1) * weights[count]

        return value

