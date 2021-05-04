class PuzzleSolver:
    def __init__(self, strategy):
        """
        :param strategy: Strategy
        """
        self._strategy = strategy

    def print_performance(self):
        print(f'{self._strategy} - Expanded Nodes: {self._strategy.num_expanded_nodes}')

    def print_solution(self):
        print('Solution:')
        for s in self._strategy.solution:
            print(s)

    def run(self):
        if not self._strategy.start.is_solvable():
            raise RuntimeError('This puzzle is not solvable')

        self._strategy.do_algorithm()


class Strategy:
    num_expanded_nodes = 0
    solution = None

    def do_algorithm(self):
        raise NotImplemented


class BreadthFirst(Strategy):
    def __init__(self, initial_puzzle):
        """
        :param initial_puzzle: Puzzle
        """
        self.start = initial_puzzle

    def __str__(self):
        return 'Breadth First'

    def do_algorithm(self):
        queue = [[self.start]]
        expanded = []
        num_expanded_nodes = 0
        path = None

        while queue:
            path = queue[0]
            queue.pop(0)  # dequeue (FIFO)
            end_node = path[-1]

            if end_node.position in expanded:
                continue

            for move in end_node.get_moves():
                if move.position in expanded:
                    continue
                queue.append(path + [move])  # add new path at the end of the queue

            expanded.append(end_node.position)
            num_expanded_nodes += 1

            if end_node.position == end_node.PUZZLE_END_POSITION:
                break

        self.num_expanded_nodes = num_expanded_nodes
        self.solution = path


class AStar(Strategy):
    def __init__(self, initial_puzzle):
        """
        :param initial_puzzle: Puzzle
        """
        self.start = initial_puzzle

    def __str__(self):
        return 'A*'

    @staticmethod
    def _calculate_new_heuristic(move, end_node):
        return move.heuristic_manhattan_distance() - end_node.heuristic_manhattan_distance()

    def do_algorithm(self):
        queue = [[self.start.heuristic_manhattan_distance(), self.start]]
        expanded = []
        num_expanded_nodes = 0
        path = None

        while queue:
            i = 0
            for j in range(1, len(queue)):
                if queue[i][0] > queue[j][0]:  # minimum
                    i = j

            path = queue[i]
            queue = queue[:i] + queue[i + 1:]
            end_node = path[-1]

            if end_node.position == end_node.PUZZLE_END_POSITION:
                break
            if end_node.position in expanded:
                continue

            for move in end_node.get_moves():
                if move.position in expanded:
                    continue
                new_path = [path[0] + self._calculate_new_heuristic(move, end_node)] + path[1:] + [move]
                queue.append(new_path)
                expanded.append(end_node.position)

            num_expanded_nodes += 1

        self.num_expanded_nodes = num_expanded_nodes
        self.solution = path[1:]


class Puzzle:
    def __init__(self, position):
        """
        :param position: a list of lists representing the puzzle matrix
        """
        self.position = position
        self.PUZZLE_NUM_ROWS = len(position)
        self.PUZZLE_NUM_COLUMNS = len(position[0])
        self.PUZZLE_END_POSITION = self._generate_end_position()

    def __str__(self):
        """
        Print in console as a matrix
        """
        puzzle_string = '—' * 13 + '\n'
        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                puzzle_string += '│{0: >2}'.format(str(self.position[i][j]))
                if j == self.PUZZLE_NUM_COLUMNS - 1:
                    puzzle_string += '│\n'

        puzzle_string += '—' * 13 + '\n'
        return puzzle_string

    def _generate_end_position(self):
        """
        Example end position in 4x4 puzzle
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
        """
        end_position = []
        new_row = []

        for i in range(1, self.PUZZLE_NUM_ROWS * self.PUZZLE_NUM_COLUMNS + 1):
            new_row.append(i)
            if len(new_row) == self.PUZZLE_NUM_COLUMNS:
                end_position.append(new_row)
                new_row = []

        end_position[-1][-1] = 0
        return end_position

    def _swap(self, x1, y1, x2, y2):
        """
        Swap the positions between two elements
        """
        puzzle_copy = [list(row) for row in self.position]  # copy the puzzle
        puzzle_copy[x1][y1], puzzle_copy[x2][y2] = puzzle_copy[x2][y2], puzzle_copy[x1][y1]

        return puzzle_copy

    @staticmethod
    def _is_odd(num):
        return num % 2 != 0

    @staticmethod
    def _is_even(num):
        return num % 2 == 0

    def _get_blank_space_row_counting_from_bottom(self):
        zero_row, _ = self._get_coordinates(0)  # blank space
        return self.PUZZLE_NUM_ROWS - zero_row

    def _get_coordinates(self, tile, position=None):
        """
        Returns the i, j coordinates for a given tile
        """
        if not position:
            position = self.position

        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                if position[i][j] == tile:
                    return i, j

        return RuntimeError('Invalid tile value')

    def _get_inversions_count(self):
        inv_count = 0
        puzzle_list = [number for row in self.position for number in row if number != 0]

        for i in range(len(puzzle_list)):
            for j in range(i + 1, len(puzzle_list)):
                if puzzle_list[i] > puzzle_list[j]:
                    inv_count += 1

        return inv_count

    def get_moves(self):
        """
        Returns a list of all the possible moves
        """
        moves = []
        i, j = self._get_coordinates(0)  # blank space

        if i > 0:
            moves.append(Puzzle(self._swap(i, j, i - 1, j)))  # move up

        if j < self.PUZZLE_NUM_COLUMNS - 1:
            moves.append(Puzzle(self._swap(i, j, i, j + 1)))  # move right

        if j > 0:
            moves.append(Puzzle(self._swap(i, j, i, j - 1)))  # move left

        if i < self.PUZZLE_NUM_ROWS - 1:
            moves.append(Puzzle(self._swap(i, j, i + 1, j)))  # move down

        return moves

    def heuristic_misplaced(self):
        """
        Counts the number of misplaced tiles
        """
        misplaced = 0

        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                if self.position[i][j] != self.PUZZLE_END_POSITION[i][j]:
                    misplaced += 1

        return misplaced

    def heuristic_manhattan_distance(self):
        """
        Counts how much is a tile misplaced from the original position
        """
        distance = 0

        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                i1, j1 = self._get_coordinates(self.position[i][j], self.PUZZLE_END_POSITION)
                distance += abs(i - i1) + abs(j - j1)

        return distance

    def is_solvable(self):
        # 1. If N is odd, then puzzle instance is solvable if number of inversions is even in the input state.
        # 2. If N is even, puzzle instance is solvable if
        #    - the blank is on an even row counting from the bottom (second-last, fourth-last, etc.)
        #      and number of inversions is odd.
        #    - the blank is on an odd row counting from the bottom (last, third-last, fifth-last, etc.)
        #    and number of inversions is even.
        # 3. For all other cases, the puzzle instance is not solvable.

        inversions_count = self._get_inversions_count()
        blank_position = self._get_blank_space_row_counting_from_bottom()

        if self._is_odd(self.PUZZLE_NUM_ROWS) and self._is_even(inversions_count):
            return True
        elif self._is_even(self.PUZZLE_NUM_ROWS) and self._is_even(blank_position) and self._is_odd(inversions_count):
            return True
        elif self._is_even(self.PUZZLE_NUM_ROWS) and self._is_odd(blank_position) and self._is_even(inversions_count):
            return True
        else:
            return False


if __name__ == '__main__':
    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]])

    for strategy in [BreadthFirst, AStar]:
        p = PuzzleSolver(strategy(puzzle))
        p.run()
        p.print_performance()
        p.print_solution()
