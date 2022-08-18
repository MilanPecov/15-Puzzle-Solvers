from abc import ABC, abstractmethod

from fifteen_puzzle_solvers.puzzle import Puzzle


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
    def __init__(self, initial_puzzle):
        """
        :param initial_puzzle: Puzzle
        """
        self.start = initial_puzzle

    def __str__(self):
        return 'Breadth First'

    def solve_puzzle(self):
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


class AStar(Strategy):
    HEURISTIC_MANHATTAN_DISTANCE, HEURISTIC_MISPLACED = 'manhattan_distance', 'misplaced'
    HEURISTIC_CONSTANTS = [HEURISTIC_MANHATTAN_DISTANCE, HEURISTIC_MISPLACED]

    # functions that can be selected to calculate the heuristic value
    heuristic_functions = {
        HEURISTIC_MANHATTAN_DISTANCE: Puzzle.heuristic_manhattan_distance.__name__,
        HEURISTIC_MISPLACED: Puzzle.heuristic_misplaced.__name__
    }

    def __init__(self, initial_puzzle, heuristic=None):
        """
        :param initial_puzzle: Puzzle
        :param heuristic: 'manhattan_distance' (default) or 'misplaced'
        """
        self.start = initial_puzzle
        self.heuristic_function = self.heuristic_functions[self.HEURISTIC_MANHATTAN_DISTANCE]

        if heuristic:
            if heuristic not in self.HEURISTIC_CONSTANTS:
                raise RuntimeError(f'Invalid Heuristic Function Name. Must be {self.HEURISTIC_CONSTANTS}')
            self.heuristic_function = self.heuristic_functions[heuristic]

    def __str__(self):
        return 'A*'

    def _calculate_new_heuristic(self, move, end_node):
        """
        Heuristic that calculates how good the current move is

        :param move: Puzzle
        :param end_node: Puzzle
        :return: heuristic value (integer)
        """
        return getattr(move, self.heuristic_function)() - getattr(end_node, self.heuristic_function)()

    def solve_puzzle(self):
        # Each sublist in the queue is a path to be explored and the first element of the path
        # is the total heuristic (integer) value for that path
        queue = [[self.start.heuristic_manhattan_distance(), self.start]]
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
