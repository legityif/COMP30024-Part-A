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
import sys
import copy
sys.path.append("/search")
from search import node

BOARD_SIZE = 7
OFFSETS = [(0,1), (-1,1), (-1,0), (0,-1), (1,-1), (1,0)]

#def search(input: dict[tuple, tuple]) -> list[tuple]:
def search(input):
    initial_node = node.Node(boardify(input), 0, 0, [])
    
    queue = [initial_node]
    
    while queue:
        heapq.heapify(queue)
        curr = heapq.heappop(queue)
        # print(curr)
        if get_score(curr.board, 'b', BOARD_SIZE)==0:
            return curr.moves
        # for every red cell
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if curr.board[r][c]:
                    if curr.board[r][c][0]=="r": 
                        # for every direction 
                        for dr, dc in OFFSETS:
                            curr_child_board = copy.deepcopy(curr.board)
                            power = curr.board[r][c][1]
                            old_r = r
                            old_c = c
                            while power>0:
                                new_r, new_c = (r+dr)%BOARD_SIZE, (c+dc)%BOARD_SIZE
                                if curr_child_board[new_r][new_c]==None:
                                    curr_child_board[new_r][new_c] = ("r", 1)
                                else:
                                    curr_child_board[new_r][new_c] = ("r", curr_child_board[new_r][new_c][1]+1)
                                r, c = new_r, new_c
                                power-=1
                            curr_child_board[old_r][old_c] = None
                            r, c = old_r, old_c
                            curr_move_copy = copy.deepcopy(curr.moves)
                            curr_move_copy.append([r, c, dr, dc])
                            child_node = node.Node(curr_child_board, curr.path_cost+1, 0, curr_move_copy)
                            queue.append(child_node)
                        print(curr.path_cost)

def heuristic(r, cs):
    pass

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

def get_neighbours(board, r, c, board_size):
    """ 
    finds all occupied neighbours of given cell r and c
    returns:
        list of neighbour coordinates
    """
    neighbours = []
    for dr, dc in OFFSETS:
        new_r, new_c = r+dr, c+dc
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
    for r in range(board_size):
        for c in range(board_size):
            if board[r][c]:
                if board[r][c][0] == player:
                    total_score += board[r][c][1]
    return total_score
