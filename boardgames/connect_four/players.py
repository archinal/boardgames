from math import inf

from boardgames.common.models import AIPlayer, HumanPlayer, Result
from .board import Tiles

class HumanConnectFourPlayer(HumanPlayer):
    pass


class AIConnectFourPlayer(AIPlayer):
    def get_value_for_board(self, board, player):
        winner = board.get_winner()
        if Result.result_to_player_number(winner) == player.number:
            return self.winning_move_score
        elif winner == Result.NO_WINNER:
            # No winner
            return 0
        else:
            return -1 * self.winning_move_score

