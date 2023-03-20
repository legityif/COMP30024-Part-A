from .utils import render_board
from collections import defaultdict
    
BOARD_SIZE = 7

class Node:
    def __init__(self, board, path_cost, heuristic_cost, moves):
        self.board = board
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost
        self.moves = moves
    
    def deboardify(self, board):
        dict = defaultdict()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j]:
                    dict[(i, j)] = board[i][j]
        return dict
    
    def __lt__(self, other):
        return self.path_cost+self.heuristic_cost < other.path_cost+other.heuristic_cost

    def __str__(self):
        return "Board: \n" + render_board(self.deboardify(self.board), ansi=True) + "\n" + " Path Cost: " + str(self.path_cost) + " Heuristic Cost: " + str(self.heuristic_cost) + " Moves: " + str(self.moves) + "\n"