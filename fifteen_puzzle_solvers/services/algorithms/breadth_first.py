from typing import List

from fifteen_puzzle_solvers.domain import Puzzle
from fifteen_puzzle_solvers.services.algorithms.base import IStrategy


class BreadthFirst(IStrategy):
    def __init__(self, initial_puzzle: Puzzle):
        self.start = initial_puzzle
        self.end_position = initial_puzzle.generate_end_position(len(initial_puzzle.position))

    def __str__(self):
        return 'Breadth First'

    def solve_puzzle(self) -> List[Puzzle]:
        queue = [[self.start]]
        path = []
        expanded = set()  # Use a set for faster lookups
        num_expanded_nodes = 0

        while queue:
            path = queue.pop(0)
            end_node = path[-1]

            if tuple(map(tuple, end_node.position)) in expanded:
                continue

            for move in end_node.get_moves():
                if tuple(map(tuple, move.position)) in expanded:
                    continue
                queue.append(path + [move])

            expanded.add(tuple(map(tuple, end_node.position)))
            num_expanded_nodes += 1

            if end_node.position == self.end_position:
                break

        self.num_expanded_nodes = num_expanded_nodes
        self.solution = path
        return self.solution
