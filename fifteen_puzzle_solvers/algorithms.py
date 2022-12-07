from abc import ABC, abstractmethod
from typing import List

from puzzle import Puzzle


class Strategy(ABC):
    """
    Performance properties of the different strategies (algorithms) to solve the puzzle
    """

    num_expanded_nodes = 0  # how many nodes in the search tree the algorithms needs to expand to solve the puzzle
    solution = None  # the sequence of operations to solve the puzzle

    @abstractmethod
    def solve_puzzle(self):
        """
        The algorithm to solve the puzzle

        :return: List with Puzzle objects
        """
        raise NotImplemented


class BreadthFirst(Strategy):
    """
    Implements a breadth-first search algorithm to solve a fifteen puzzle.
    It takes an initial puzzle state as input and returns a list of Puzzle objects
    that represents the sequence of moves to solve the puzzle.
    """
    def __init__(self, initial_puzzle: Puzzle):
        self.start = initial_puzzle

    def __str__(self):
        return 'Breadth First'

    def solve_puzzle(self) -> List[Puzzle]:
        """
        Uses a queue list to keep track of the paths that need to be explored.
        The algorithm  begins by adding the initial puzzle state to the queue list. Then, it repeatedly takes the first
        path from the queue list, gets all the possible moves from the last position in the path, and adds the new paths
        to the end of the queue list. This process continues until the end position of the puzzle is reached or
        there are no more paths to explore.

        Also keeps track of the positions that have been explored using the expanded list, in order to avoid circular
        logic.

        It also increments a counter for the number of expanded nodes, which is stored in the num_expanded_nodes
        attribute

        Finally, it sets the solution attribute to the concatenation of all the paths in the queue list that lead to the
        end position of the puzzle.
        """

        queue = [[self.start]]  # list of lists with Puzzle objects. Each sublist is a path to be explored
        path = []  # the current path that we want to explore
        expanded = []  # keeps track on the positions that have already been explored
        num_expanded_nodes = 0  # counter used for performance analysis

        while queue:
            path = queue[0]  # take the first path - this is a list with Puzzle objects
            queue.pop(0)  # dequeue (FIFO)
            end_node = path[-1]  # the last position in the path that we are exploring

            if end_node.position in expanded:  # avoid circular logic
                continue

            for move in end_node.get_moves():  # loop through all the possible moves for the current position
                if move.position in expanded:  # avoid circular logic
                    continue
                queue.append(path + [move])  # add the path with the new positions at the end of the queue

            expanded.append(end_node.position)  # all the moves for this positions are now in the queue
            num_expanded_nodes += 1

            if end_node.position == end_node.PUZZLE_END_POSITION:  # the last position in our path is the end position
                break

        # set base class values
        self.num_expanded_nodes = num_expanded_nodes  # increment the performance counter
        self.solution = path

        return self.solution


class AStar(Strategy):
    """
    Implements an A* search algorithm to solve a fifteen puzzle. The AStar class has a few additional attributes and
    methods compared to the BreadthFirst class, namely manhattan_distance and misplaced,
    which are string constants used to specify the heuristic function to use for the A* search algorithm.
    """

    HEURISTIC_MANHATTAN_DISTANCE, HEURISTIC_MISPLACED = 'manhattan_distance', 'misplaced'
    HEURISTIC_CONSTANTS = [HEURISTIC_MANHATTAN_DISTANCE, HEURISTIC_MISPLACED]

    # functions that can be selected to calculate the heuristic value
    heuristic_functions = {
        HEURISTIC_MANHATTAN_DISTANCE: Puzzle.heuristic_manhattan_distance.__name__,
        HEURISTIC_MISPLACED: Puzzle.heuristic_misplaced.__name__
    }

    def __init__(self, initial_puzzle: Puzzle, heuristic: str = None):
        """
        Takes an initial puzzle state and an optional heuristic function name as input.
        """

        self.start = initial_puzzle
        self.heuristic_function = self.heuristic_functions[self.HEURISTIC_MANHATTAN_DISTANCE]

        if heuristic:
            if heuristic not in self.HEURISTIC_CONSTANTS:
                raise RuntimeError(f'Invalid Heuristic Function Name. Must be {self.HEURISTIC_CONSTANTS}')
            self.heuristic_function = self.heuristic_functions[heuristic]

    def __str__(self):
        return 'A*'

    def _calculate_new_heuristic(self, move: Puzzle, end_node: Puzzle) -> int:
        """
        Heuristic that calculates how good the current move is
        """

        return getattr(move, self.heuristic_function)() - getattr(end_node, self.heuristic_function)()

    def solve_puzzle(self) -> List[Puzzle]:
        """
        Uses a queue list to keep track of the paths that need to be explored. However, instead of simply adding the
        paths to the end of the queue list, it calculates the total heuristic value of each path and adds the path
        along with its heuristic value to the queue list. This allows the solve_puzzle method to find the path with the
        lowest heuristic value and explore that path first.

        _calculate_new_heuristic method is used to calculate the heuristic value of each new move and add it to the
        total heuristic value of the path.

        It also increments a counter for the number of expanded nodes, which is stored in the num_expanded_nodes
        attribute.

        Finally, it sets the solution attribute to the concatenation of all the paths in the queue list that lead
        to the end position of the puzzle.
        """

        # Each sublist in the queue is a path to be explored and the first element of the path
        # is the total heuristic (integer) value for that path
        queue = [[getattr(self.start, self.heuristic_function)(), self.start]]
        path = []  # the current path that we want to explore
        expanded = []  # keeps track on the positions that have already been explored
        num_expanded_nodes = 0  # counter used for performance analysis

        while queue:
            # find which path in the queue has the lowest heuristic value
            i = 0
            for j in range(1, len(queue)):
                if queue[i][0] > queue[j][0]:  # minimum
                    i = j

            path = queue[i]  # take the path with the lowest heuristic value
            queue = queue[:i] + queue[i + 1:]  # remove the path from the queue
            end_node = path[-1]  # the last position in the path that we are exploring

            if end_node.position == end_node.PUZZLE_END_POSITION:  # the last position in our path is the end position
                break
            if end_node.position in expanded:  # avoid circular logic
                continue

            for move in end_node.get_moves():  # loop through all the possible moves for the current position
                if move.position in expanded:
                    continue

                # add the path with the new positions and their heuristics at the end of the queue
                new_path = [path[0] + self._calculate_new_heuristic(move, end_node)] + path[1:] + [move]
                queue.append(new_path)
                expanded.append(end_node.position)

            num_expanded_nodes += 1  # increment the performance counter

        # set base class values
        self.num_expanded_nodes = num_expanded_nodes
        self.solution = path[1:]

        return self.solution
