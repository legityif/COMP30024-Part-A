# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

# """
# This is the entry point for your submission. The input is a dictionary
# of board cell states, where the keys are tuples of (r, q) coordinates, and
# the values are tuples of (p, k) cell states. The output should be a list of 
# actions, where each action is a tuple of (r, q, dr, dq) coordinates.

# See the specification document for more details.
# """

# The render_board function is useful for debugging -- it will print out a 
# board state in a human-readable format. Try changing the ansi argument 
# to True to see a colour-coded version (if your terminal supports it).

# Here we're returning "hardcoded" actions for the given test.csv file.
# Of course, you'll need to replace this with an actual solution...
    

# from .utils import render_board
# print(render_board(input, ansi=True))

import heapq
from .node import *

BOARD_SIZE = 7
OFFSETS = ((0,1), (-1,1), (-1,0), (0,-1), (1,-1), (1,0))

def search(input):
    """
    Performs a A* search with a heuristic function on the given board.
    """
    initial_board = boardify(input)
    initial_node = Node(initial_board, 0, heuristic(initial_board), [])
    queue = [initial_node]

    # visited = set(tupleify(initial_board))
    while queue:
        heapq.heapify(queue)
        curr = heapq.heappop(queue)
        print(curr.moves)
                
        if get_score(curr.board, 'b', BOARD_SIZE)==0:
            return curr.moves
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if curr.board[r][c] and curr.board[r][c][0]=="r":
                    for dr, dc in OFFSETS:
                        curr_child_board = [row[:] for row in curr.board]
                        power = curr.board[r][c][1]
                        old_r, old_c = r, c
                        spread_in_dir(curr_child_board, dr, dc, r, c, old_r, old_c, power)
                        curr_move_copy = curr.moves+[[r, c, dr, dc]]
                        child_node = Node(curr_child_board, curr.path_cost+1, heuristic(curr_child_board), curr_move_copy)
                        # check if current state is in visited state, but with a lower cost, replace visited state with identical state with lower cost
                        # if tupleify(child_node.board) not in visited:
                        queue.append(child_node)
                        # visited.add(tupleify(child_node.board))

def spread_in_dir(curr_child_board, dr, dc, r, c, old_r, old_c, power):
    """
    spreads a cell in the given direction.
    returns: 
        void
    """
    while power>0:
        new_r, new_c = (r+dr)%BOARD_SIZE, (c+dc)%BOARD_SIZE
        if curr_child_board[new_r][new_c]==None:
            curr_child_board[new_r][new_c] = ("r", 1)
        else:
            if curr_child_board[new_r][new_c][1]+1 > 6:
                curr_child_board[new_r][new_c] = None
            else:
                curr_child_board[new_r][new_c] = ("r", curr_child_board[new_r][new_c][1]+1)
        r, c = new_r, new_c
        power-=1
    curr_child_board[old_r][old_c] = None
    r, c = old_r, old_c

def heuristic(board):
    """
    returns heuristic value for a given board
    returns:
        heuristic value as int
    """
    total_blue = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c]:
                if board[r][c][0]=='b':
                    total_blue += 1
    return total_blue

def boardify(input):
    """
    converts a dictionary of board cell states to a 2D list of lists
    where each list represents a board cell.
    returns:
        list of lists
    """
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for ((r, c), (player, power)) in input.items():
        board[r][c] = (player, power)
    return board

def tupleify(board):
    """
    converts a 2D list of lists to a dictionary of board cell states
    returns:
        dictionary of board cell states
    """
    return tuple(tuple(row) for row in board)

def get_score(board, player, board_size):
    """ 
    gets player total board score, player is either 'b' or 'r' 
    returns:
        total score as int
    """
    total_score = 0
    for r in range(board_size):
        for c in range(board_size):
            if board[r][c]:
                if board[r][c][0] == player:
                    total_score += board[r][c][1]
    return total_score
