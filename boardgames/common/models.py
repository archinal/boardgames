from abc import abstractmethod
from math import inf, sqrt
import time


class Game:
    players = []
    board = None
    turn_number = 0
    turn_limit = 1000
    branching_factor = 100

    def run(self):
        self.commence_game()

        while not self.board.is_terminal() and self.turn_number < self.turn_limit:
            player_to_move = self.get_whose_turn()
            move = player_to_move.get_move_for_game(self)
            self.board.apply_move(move)
            self.turn_number += 1

        self.terminate_game(self.board.get_winner())

    def commence_game(self):
        pass

    def terminate_game(self, winner):
        self.board.print_board()
        if winner is not Result.NO_WINNER:
            print('Player {player} wins in {turns} turns!'.format(player=winner, turns=self.turn_number))
        else:
            print('It\'s a draw!')

    def get_whose_turn(self, override_turn_number=None):
        num_players = len(self.players)
        turn = (self.turn_number if override_turn_number is None else override_turn_number) % num_players
        return self.players[turn]

    @abstractmethod
    def print_state(self):
        pass

    def is_legal_move(self, move, player):
        # TODO: Check correct player
        return self.board.is_legal_move(move)

    def get_legal_moves(self, override_turn=None):
        return self.board.get_legal_moves(self.get_whose_turn(override_turn))

    @abstractmethod
    def string_to_move(self, string, player):
        pass

    def get_branching_factor(self):
        return self.branching_factor


class Board:
    @abstractmethod
    def apply_move(self, move):
        pass

    @abstractmethod
    def undo_move(self, move):
        pass

    @abstractmethod
    def is_terminal(self):
        pass

    @abstractmethod
    def get_winner(self):
        pass

    @abstractmethod
    def print_board(self):
        pass

    @abstractmethod
    def is_legal_move(self, move):
        pass

    @abstractmethod
    def get_legal_moves(self, player):
        pass


class Player:
    def __init__(self, number):
        self.number = number

    def get_name(self):
        return 'Player {number}'.format(number=str(self.number + 1))

    @abstractmethod
    def get_move_for_game(self, game):
        pass


class HumanPlayer(Player):
    def get_move_for_game(self, game):
        game.print_state()
        move = None
        while move is None or not game.is_legal_move(move, self):
            move_str = input('> ')
            move = game.string_to_move(move_str, self)
            if move is not None and game.is_legal_move(move, self):
                return move
            else:
                print('Invalid move')


class AIPlayer(Player):
    max_soft_thinking_time = 1  # Seconds
    winning_move_score = inf

    @abstractmethod
    def get_value_for_board(self, board, player):
        pass

    def get_move_for_game(self, game):
        game.print_state()
        legal_moves = game.get_legal_moves()
        # Intentionally error out straight away if no legal moves exist
        best_move = legal_moves[0]
        current_time = time.time()
        branching_factor = game.get_branching_factor()
        branching_factor_sqrt = sqrt(branching_factor)
        min_depth = 2
        max_depth = 100
        depth = 0
        estimated_next_duration = 0
        while (estimated_next_duration < self.max_soft_thinking_time and depth < max_depth) or depth <= min_depth:
            depth += 1
            best_move = self.alpha_beta_from_root(legal_moves, game, depth, game.turn_number)
            search_ended_time = time.time()
            previous_search_duration = search_ended_time - current_time
            estimated_next_duration = previous_search_duration * branching_factor_sqrt
            current_time = time.time()
        print('> ' + str(best_move.dest_col))
        return best_move

    def alpha_beta_from_root(self, legal_moves, game, max_depth, turn_number):
        num_valid_moves = len(legal_moves)
        best_move = legal_moves[0]
        alpha = -inf

        if num_valid_moves is 1:
            return best_move
        else:
            for move in legal_moves:
                game.board.apply_move(move)
                val_for_board = -1 * self.alpha_beta(game, max_depth - 1, alpha, inf, turn_number + 1, max_depth)
                game.board.undo_move(move)
                if val_for_board > alpha:
                    alpha = val_for_board
                    best_move = move

        return best_move

    def alpha_beta(self, game, depth, alpha, beta, turn_number, max_depth):
        is_terminal = game.board.is_terminal()
        if depth == 0 or is_terminal:
            return -1 * self.winning_move_score + depth if is_terminal else \
                self.get_value_for_board(game.board, game.get_whose_turn(turn_number))
        else:
            best_value = -inf
            valid_moves = game.get_legal_moves(turn_number)
            for move in valid_moves:
                game.board.apply_move(move)
                next_turn = turn_number + 1
                board_val = -1 * self.alpha_beta(game, depth - 1, -beta, -alpha, next_turn, max_depth)
                game.board.undo_move(move)
                if board_val > best_value:
                    best_value = board_val
                alpha = alpha if alpha > board_val else board_val
                if alpha >= beta:
                    # Cutoff
                    break
            return best_value


class Result:
    NO_WINNER = 0
    PLAYER_1 = 1
    PLAYER_2 = 2

    RESULT_TO_PLAYER_NUMBER = {
        NO_WINNER: 0,
        PLAYER_1: 1,
        PLAYER_2: 2,
    }

    PLAYER_NUMBER_TO_RESULT = {
        0: NO_WINNER,
        1: PLAYER_1,
        2: PLAYER_2,
    }

    @staticmethod
    def result_to_player_number(result):
        return Result.RESULT_TO_PLAYER_NUMBER[result]

    @staticmethod
    def player_number_to_result(number):
        return Result.PLAYER_NUMBER_TO_RESULT[number]

