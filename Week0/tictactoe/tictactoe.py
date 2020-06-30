"""
Tic Tac Toe Player
"""

import math
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
    countX = 0
    countO = 0
    for row in board:
        for cell in row:
            if cell == X:
                countX += 1
            elif cell == O:
                countO += 1
    if countO > countX or countO == countX:
        return X
    elif countX > countO:
        return O
    else:
        return None

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # a set to store all available position (empty position)
    possible_actions = set()
    # loop through currend board state to add all empty posion in set
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i,j))
    return possible_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # unpack i j values of action(tuple)
    p = player(board)
    (i, j) = action
    copied_board = copy.deepcopy(board)
    # if action indicates place that is not empty, return valueError
    if not board[i][j] == EMPTY:
        raise ValueError("Invalid Action")
    # deepcopy current board state to take action on it
    # implement no change on the current board
    else: 
        copied_board[i][j] = p
    return copied_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] == board[0][2] != None:
        return board[0][0]
    elif board[1][0] == board[1][1] == board[1][2] != None: 
        return board[1][0]
    elif board[2][0] == board[2][1] == board[2][2] != None:
        return board[2][0]
    elif board[0][0] == board[1][0] == board[2][0] != None:
        return board[0][0]
    elif board[0][1] == board[1][1] == board[2][1] != None:
        return board[0][1]
    elif board[0][2] == board[1][2] == board[2][2] != None:
        return board[0][2]
    elif board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    # If all cells are filled
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True          
                

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    flag_win = winner(board)
    if flag_win == X:
        return 1
    elif flag_win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # because X player has the fiset step so his goal is to maximize score; on the contrary, O player should minimize score
    current_player = player(board)
    # X player: pick action that leads to the highest of minValue(result(state, action))
    if current_player == X:
        final_selection = None
        v = float("-inf")
        for action in actions(board):
            temp_min_Value = minValue(result(board, action))
            # if find a temperary highest, update local variables 
            if temp_min_Value > v:
                v = temp_min_Value
                final_selection = action
        return final_selection
    
    # O player: pick action that leads to the lowest of maxValue(result(state, action))
    if current_player == O:
        final_selection = None
        v = float("inf")
        for action in actions(board):
            temp_max_Value = maxValue(result(board, action))
            # if find a temperary highest, update local variables 
            if temp_max_Value < v:
                v = temp_max_Value
                final_selection = action
        return final_selection

# define function max-value
def maxValue(board):
    if terminal(board):
        return utility(board)
    v = -float('inf')
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v

# define function min-value    
def minValue(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    return v