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
    

from .utils import render_board
import heapq
from search import Node

BOARD_SIZE = 7
board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def heuristic(i, j):
    pass

def get_score(board, player, board_size):
    """
    returns the score of the given player on the given board
    """
    score = 0
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] is not None:
                if board[i][j][0] == player:
                    score += board[i][j][1]
    return score

def search(input: dict[tuple, tuple]) -> list[tuple]:
    print(input)
    print(render_board(input, ansi=True))
    for ((r, q), (player, power)) in input.items():
        board[r][q] = (player, power)

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            print(f"Neighbours of cell {i, j} : {get_neighbours(board, i, j, BOARD_SIZE)}")
            
    # SOLVE SEARCHING
    # use normal array for bfs
    # use heapq for priority q operations on array
    # use heapq methods heapq.heappop, heapq.heappush, 
            

    print(board)
    print(f"total blue score : {get_score(board, 'b', BOARD_SIZE)}")
    print(f"total red score : {get_score(board, 'r', BOARD_SIZE)}")
    
    return []

    # return [
    #     (5, 6, -1, 1),
    #     (3, 1, 0, 1),
    #     (3, 2, -1, 1),
    #     (1, 4, 0, -1),
    #     (1, 3, 0, -1)
    # ]

def get_neighbours(board, r, c, board_size):
    """ 
    finds all occupied neighbours of given cell r and c
    returns:
        list of neighbour coordinates
    """
    OFFSETS = [(0,1), (-1,1), (-1,0), (0,-1), (1,-1), (1,0)]
    neighbours = []
    for i, j in OFFSETS:
        new_r, new_c = r+i, c+j
        if 0<=new_r<board_size and 0<=new_c<board_size and board[new_r][new_c]:
            neighbours.append((new_r, new_c))
    return neighbours
        
        
def get_score(board, player, board_size):
    """ 
    gets player total board score, player is either 'b' or 'r' 
    returns:
        total score as int
    """
    total_score = 0
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j]:
                if board[i][j][0] == player:
                    total_score += board[i][j][1]
    return total_score
