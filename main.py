import pprint

PUZZLE_END = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]  # 4x4


class PuzzleSolver:
    def __init__(self, strategy):
        self._strategy = strategy

    def run(self):
        self._strategy.do_algorithm()


class PuzzleSize:
    PUZZLE_NUM_ROWS = len(PUZZLE_END)
    PUZZLE_NUM_COLUMNS = len(PUZZLE_END[0])


class StrategyUtils(PuzzleSize):
    @staticmethod
    def _to_list(puzzle):
        """
        Convert nested tuple to nested list
        """
        return [list(row) for row in puzzle]

    @staticmethod
    def _get_blank_space_coordinates(puzzle):
        """
        Returns the i, j coordinates of the 0
        """
        i = 0
        while 0 not in puzzle[i]:
            i += 1
        j = puzzle[i].index(0)

        return i, j

    def _swap(self, puzzle, x1, y1, x2, y2):
        """
        Swap the positions between two elements
        """
        p = self._to_list(puzzle)  # copy the puzzle
        p[x1][y1], p[x2][y2] = p[x2][y2], p[x1][y1]

        return p

    def _get_moves(self, puzzle):
        """
        Returns a list of all the possible moves
        """
        moves = []
        i, j = self._get_blank_space_coordinates(puzzle)

        if i > 0:
            moves.append(self._swap(puzzle, i, j, i - 1, j))  # move up

        if j < self.PUZZLE_NUM_COLUMNS - 1:
            moves.append(self._swap(puzzle, i, j, i, j + 1))  # move right

        if j > 0:
            moves.append(self._swap(puzzle, i, j, i, j - 1))  # move left

        if i < self.PUZZLE_NUM_ROWS - 1:
            moves.append(self._swap(puzzle, i, j, i + 1, j))  # move down

        return moves


class StrategyHeuristics(PuzzleSize):
    def _heuristic_misplaced(self, puzzle):
        """
        Counts the number of misplaced tiles
        """
        misplaced = 0

        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                if puzzle[i][j] != PUZZLE_END[i][j]:
                    misplaced += 1

        return misplaced

    def _heuristic_manhattan_distance(self, puzzle):
        """
        Counts how much is a tile misplaced from the original position
        """
        distance = 0

        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                misplaced_rows_weight = abs(i - (puzzle[i][j] / self.PUZZLE_NUM_ROWS))
                misplaced_columns_weight = abs(j - (puzzle[i][j] % self.PUZZLE_NUM_COLUMNS))

                distance += misplaced_rows_weight + misplaced_columns_weight

        return distance


class Strategy(StrategyUtils, StrategyHeuristics):
    num_expanded_nodes = 0

    def do_algorithm(self):
        raise NotImplemented


class AStar(Strategy):
    def __init__(self, start):
        self.start = self._to_list(start)
        self.heuristic = self._heuristic_manhattan_distance  # optional _heuristic_misplaced

    def do_algorithm(self):
        front = [[self.heuristic(self.start), self.start]]
        expanded = []
        num_expanded_nodes = 0
        path = None

        while front:
            i = 0
            for j in range(1, len(front)):
                if front[i][0] > front[j][0]:
                    i = j
            path = front[i]
            front = front[:i] + front[i + 1:]
            end_node = path[-1]
            if end_node == PUZZLE_END:
                break
            if end_node in expanded:
                continue
            for k in self._get_moves(end_node):
                if k in expanded:
                    continue
                new_path = [path[0] + self.heuristic(k) - self.heuristic(end_node)] + path[1:] + [k]
                front.append(new_path)
                expanded.append(end_node)
            num_expanded_nodes += 1

        self.num_expanded_nodes = num_expanded_nodes
        print(f'A* - Expanded nodes: {num_expanded_nodes}')
        print('Solution:')
        pprint.PrettyPrinter().pprint(path)


class BreadthFirst(Strategy):
    def __init__(self, start):
        self.start = self._to_list(start)

    def do_algorithm(self):
        front = [[self.start]]
        expanded = []
        num_expanded_nodes = 0
        path = None

        while front:
            i = 0
            for j in range(1, len(front)):  # minimum
                if len(front[i]) > len(front[j]):
                    i = j
            path = front[i]
            front = front[:i] + front[i + 1:]
            end_node = path[-1]
            if end_node in expanded:
                continue
            for k in self._get_moves(end_node):
                if k in expanded:
                    continue
                front.append(path + [k])
            expanded.append(end_node)
            num_expanded_nodes += 1
            if end_node == PUZZLE_END:
                break

        self.num_expanded_nodes = num_expanded_nodes
        print(f'Breadth First - Expanded nodes: {num_expanded_nodes}')
        print('Solution:')
        pprint.PrettyPrinter().pprint(path)


if __name__ == '__main__':
    puzzle_start = ((4, 1, 2, 3), (5, 6, 7, 11), (8, 9, 10, 15), (12, 13, 14, 0))

    PuzzleSolver(AStar(puzzle_start)).run()
    PuzzleSolver(BreadthFirst(puzzle_start)).run()
