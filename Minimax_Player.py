from Board import BoardUtility
import random
import copy
import numpy as np


class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]),
                random.choice(["skip", "clockwise", "anticlockwise"])]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n")
        move = move.split()
        print(move)
        return [[int(move[0]), int(move[1])], int(move[2]), move[3]]


def get_neighbours(board):
    neighbours = []
    for row_i, column_i in BoardUtility.get_valid_locations(board):
        for region_i in range(1, 5):
            for rot_i in ["skip", "clockwise", "anticlockwise"]:
                neighbours.append([[row_i, column_i], region_i, rot_i])
    return neighbours


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth

    def calculate_board_value(self, board):
        if BoardUtility.has_player_won(board, self.piece):
            return float('inf')
        elif BoardUtility.has_player_won(board, 2 - self.piece):
            return float('-inf')
        elif BoardUtility.is_draw(board):
            return 0

        value = 0
        for r in range(0, 6):
            for c in range(0, 4):
                if board[r][c] == board[r][c + 1] == board[r][c + 2] or board[c][r] == board[c + 1][r] == board[c + 2][
                    r]:
                    if board[r][c] == self.piece:
                        value += 10
                    elif board[r][c] == 3 - self.piece:
                        value -= 10
                elif board[r][c] == board[r][c + 1] or board[c][r] == board[c + 1][r]:
                    if board[r][c] == self.piece:
                        value += 4
                    elif board[r][c] == 3 - self.piece:
                        value -= 4
        for c in range(1, 5):
            for r in range(1, 5):
                if board[r][c] == board[r + 1][c + 1] == board[r - 1][c - 1]:
                    if board[r][c] == self.piece:
                        value += 10
                    elif board[r][c] == 3 - self.piece:
                        value -= 10
                elif board[r][c] == board[r + 1][c + 1] or board[r][c] == board[r - 1][c - 1]:
                    if board[r][c] == self.piece:
                        value += 4
                    elif board[r][c] == 3 - self.piece:
                        value -= 4
        for r in range(0, 6):
            for c in range(0, 6):
                if board[r][c] == self.piece:
                    value += r * (5 - r) + c * (5 - c)
                elif board[r][c] == 3 - self.piece:
                    value += r * (5 - r) + c * (5 - c)

        return value

    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimax algorithm
        alpha = -np.inf
        beta = np.inf
        best_move_value = -np.inf
        for neighbour in get_neighbours(board):
            copy_board = copy.deepcopy(board)
            [row1, col1], region1, rotation1 = neighbour
            BoardUtility.make_move(copy_board, row1, col1, region1, rotation1, self.piece)
            move_value = self.minimax_play(copy_board, 1, player=3 - self.piece)
            if move_value > best_move_value:
                best_move_value = move_value
                row, col, region, rotation = row1, col1, region1, rotation1

            if best_move_value >= beta:
                return [[row, col], region, rotation]
            alpha = max(alpha, best_move_value)

        return [[row, col], region, rotation]

    def minimax_play(self, board, depth, player, alpha=float('-inf'), beta=float('inf')):
        if depth >= self.depth or BoardUtility.is_terminal_state(board):
            return self.calculate_board_value(board)

        copy_board = copy.deepcopy(board)

        if player == self.piece:
            max_value = -np.inf
            for neighbour in get_neighbours(board):
                [row1, col1], region1, rotation1 = neighbour
                BoardUtility.make_move(copy_board, row1, col1, region1, rotation1, player)
                value = self.minimax_play(copy_board, depth + 1, 3 - player, alpha, beta)
                max_value = max(max_value, value)
                if beta <= max_value:
                    break
                alpha = max(alpha, max_value)

                copy_board = copy.deepcopy(board)
            return max_value

        else:
            min_value = np.inf
            for neighbour in get_neighbours(board):
                [row1, col1], region1, rotation1 = neighbour
                BoardUtility.make_move(copy_board, row1, col1, region1, rotation1, player)
                value = self.minimax_play(copy_board, depth + 1, 3 - player, alpha, beta)
                min_value = min(min_value, value)
                if min_value <= alpha:
                    break
                beta = min(beta, min_value)

                copy_board = copy.deepcopy(board)
            return min_value


class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    def calculate_board_value(self, board):
        if BoardUtility.has_player_won(board, self.piece):
            return float('inf')
        elif BoardUtility.has_player_won(board, 2 - self.piece):
            return float('-inf')
        elif BoardUtility.is_draw(board):
            return 0

        value = 0
        for r in range(0, 6):
            for c in range(0, 4):
                if board[r][c] == board[r][c + 1] == board[r][c + 2] or board[c][r] == board[c + 1][r] == board[c + 2][
                    r]:
                    if board[r][c] == self.piece:
                        value += 10
                    elif board[r][c] == 3 - self.piece:
                        value -= 10
                elif board[r][c] == board[r][c + 1] or board[c][r] == board[c + 1][r]:
                    if board[r][c] == self.piece:
                        value += 4
                    elif board[r][c] == 3 - self.piece:
                        value -= 4
        for c in range(1, 5):
            for r in range(1, 5):
                if board[r][c] == board[r + 1][c + 1] == board[r - 1][c - 1]:
                    if board[r][c] == self.piece:
                        value += 10
                    elif board[r][c] == 3 - self.piece:
                        value -= 10
                elif board[r][c] == board[r + 1][c + 1] or board[r][c] == board[r - 1][c - 1]:
                    if board[r][c] == self.piece:
                        value += 4
                    elif board[r][c] == 3 - self.piece:
                        value -= 4
        for r in range(0, 6):
            for c in range(0, 6):
                if board[r][c] == self.piece:
                    value += r * (5 - r) + c * (5 - c)
                elif board[r][c] == 3 - self.piece:
                    value += r * (5 - r) + c * (5 - c)

        return value

    def minimax_play(self, board, depth, player, alpha=float('-inf'), beta=float('inf')):
        if depth > self.depth or BoardUtility.is_terminal_state(board):
            return self.calculate_board_value(board)

        copy_board = copy.deepcopy(board)

        if player == self.piece:
            max_value = -np.inf
            for neighbour in get_neighbours(board):
                [row1, col1], region1, rotation1 = neighbour
                BoardUtility.make_move(copy_board, row1, col1, region1, rotation1, player)
                value = self.minimax_play(copy_board, depth + 1, 3 - player, alpha, beta)
                max_value = max(max_value, value)
                if beta <= max_value:
                    break
                alpha = max(alpha, max_value)

                copy_board = copy.deepcopy(board)
            return max_value

        else:
            min_value = np.inf
            for neighbour in get_neighbours(board):
                [row1, col1], region1, rotation1 = neighbour
                BoardUtility.make_move(copy_board, row1, col1, region1, rotation1, player)
                value = self.minimax_play(copy_board, depth + 1, 3 - player, alpha, beta)
                min_value = min(min_value, value)
                if min_value <= alpha:
                    break
                beta = min(beta, min_value)

                copy_board = copy.deepcopy(board)
            return min_value

    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimaxProb algorithm
        neighbours = get_neighbours(board)
        if len(neighbours) != 0 and sum(random.choices([True, False], [self.prob_stochastic, 1 - self.prob_stochastic],
                                                       k=1)):
            return random.choice(neighbours)

        alpha = -np.inf
        beta = np.inf
        best_move_value = -np.inf
        copy_board = copy.deepcopy(board)
        for neighbour in get_neighbours(board):
            [row1, col1], region1, rotation1 = neighbour
            BoardUtility.make_move(copy_board, row1, col1, region1, rotation1, self.piece)
            move_value = self.minimax_play(copy_board, 1, player=3 - self.piece)
            if move_value > best_move_value:
                best_move_value = move_value
                row, col, region, rotation = row1, col1, region1, rotation1

            copy_board = copy.deepcopy(board)
            if best_move_value >= beta:
                return [[row, col], region, rotation]
            alpha = max(alpha, best_move_value)

        return [[row, col], region, rotation]
