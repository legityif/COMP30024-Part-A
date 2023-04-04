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

from .node import *
from collections import deque

BOARD_SIZE = 7
OFFSETS = ((0,1), (-1,1), (-1,0), (0,-1), (1,-1), (1,0))


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    Performs an Iterative Deepening A* search with a heuristic function on the given board.
    """
    
    initial_board = boardify(input)
    initial_node = Node(initial_board, 0, heuristic_infinite_spread(initial_board), [])
    bound = initial_node.heuristic_cost
    while True:
        t = idastar(initial_node, 0, bound)
        if isinstance(t, list):
            return t
        bound = t
        

def idastar(node, path_cost, bound):
    """
    Idastar algorithm
    """
    total_cost = path_cost + node.heuristic_cost
    if total_cost > bound:
        return total_cost
    if get_score(node.board, 'b', BOARD_SIZE)==0:
        return node.moves

    min_cost = float('inf')
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if node.board[r][c] and node.board[r][c][0]=="r":
                for dr, dc in OFFSETS:
                    child_board = [row[:] for row in node.board]
                    power = node.board[r][c][1]
                    old_r, old_c = r, c
                    spread_in_dir(child_board, dr, dc, r, c, old_r, old_c, power)
                    if get_score(child_board, 'r', BOARD_SIZE)==0:
                            continue
                    child_node = Node(child_board, node.path_cost+1, heuristic_infinite_spread(child_board), node.moves+[[r, c, dr, dc]])
                    cost = idastar(child_node, path_cost+1, bound)
                    if isinstance(cost, list):
                        return cost
                    min_cost = min(min_cost, cost)
    return min_cost


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


def heuristic_infinite_spread(board):
    """
    Since a red cell has to be one the same "line" as a blue cell (where a line is the straight line connecting the red and blue cell)
    in order to take over the blue cell, we can find the minimum number of lines that it takes to connect all the blue cells. 
    Where two blue cells are considered to be on the same "line" if they are connected in a straight line, in either the x, y, or z direction.
    """

    # first put all the blue cells into a queue
    queue = deque()
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c]:
                if board[r][c][0]=='b':
                    queue.append((r, c))
    
    # Keep track of the marked row, column, and diagonals
    visited = {"r0": False, "r1": False, "r2": False, "r3": False, "r4": False, "r5": False, "r6": False,
               "c0": False, "c1": False, "c2": False, "c3": False, "c4": False, "c5": False, "c6": False,
               "d0": False, "d1": False, "d2": False, "d3": False, "d4": False, "d5": False, "d6": False}
    totalExpanded = 0
    
    while(queue):
        r, c = queue.popleft()
        # check if this cell has already been marked on the corresponding row, col, or diagonal
        # sum of 7 --> diagonal 0, sum of 10 --> diagonal 3, sum of 11 --> diagonal 4, sum of 12 --> diagonal 5
        # if r+c = n, where n < 7, then n is the diagonal number, otherwise, modulo it with 7   
        row = "r" + str(r)
        col = "c" + str(c)
        diag = "d" + str((r+c)%BOARD_SIZE)

        if visited[row]==True or visited[col]==True or visited[diag]==True:
            continue
        else:
            # this cell is not on a marked line, we need to spread it in all 3 directions (mark all lines as visited)
            visited[row] = True
            visited[col] = True
            visited[diag] = True
            totalExpanded += 1

    return totalExpanded


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
