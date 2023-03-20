class Node:
    def __init__(self, state, path_cost, heuristic_cost, moves):
        self.state = state
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost
        self.moves = moves
