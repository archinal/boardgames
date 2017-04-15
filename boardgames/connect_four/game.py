from boardgames.common.models import Game

from .board import ConnectFourBoard
from .move import Move


class ConnectFourGame(Game):
    def __init__(self, player_1, player_2):
        super().__init__()
        self.players = [player_1, player_2]
        self.board = ConnectFourBoard()
        self.branching_factor = self.board.NUM_COLS

    def is_legal_move(self, move, player):
        return super().is_legal_move(move, player)

    def string_to_move(self, string, player):
        try:
            col = int(string)
            col -= 1
            if col < 0 or col >= ConnectFourBoard.NUM_COLS:
                raise ValueError
            move = Move(col, player)
        except ValueError:
            move = None
        return move

    def print_state(self):
        self.board.print_board()
        print(self.get_whose_turn().get_name() + '\'s turn')
