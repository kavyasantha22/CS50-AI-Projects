"""
Tic Tac Toe Player
"""

import math
import random
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    filled = 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] != EMPTY:
                filled += 1
    if filled % 2:
        return "O"
    else:
        return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                actions.add((row, col))
    return actions


# CHECK AGAIN IS IT RANDOM OR ITERATE EVERYTHING
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if i >= len(board) or j >= len(board[0]) or i < 0 or j < 0:
        raise ValueError("Invalid move: Position is out-of-bounds")

    if board[i][j] != EMPTY:
        raise ValueError("Invalid move: Position is already taken")

    copied = copy.deepcopy(board)
    turn = player(copied)
    copied[i][j] = turn
    return copied


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]

    if board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    for row in range(len(board)):
        if board[row][0] == board[row][1] and board[row][0] == board[row][2] and board[row][0] != EMPTY:
            return board[row][0]

    for col in range(len(board[0])):
        if board[0][col] == board[1][col] and board[0][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


def minimax2(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check whose turn
    turn = player(board)

    # Initialize variable
    opt_value = float('-inf') if turn == "X" else float('inf')
    opt_action = None

    # Check whether the next game is ald over
    if terminal(board):
        return None, utility(board)

    for action in actions(board):
        # Initialize board for each move
        current_board = result(board, action)

        # Finish each board and get the value
        current_value = minimax2(current_board)[1]

        # Update minimax value
        if (turn == 'X' and current_value > opt_value) or (turn == 'O' and current_value < opt_value):
            opt_value = current_value
            opt_action = action

    return opt_action, opt_value


def minimax(board):
    return minimax2(board)[0]
