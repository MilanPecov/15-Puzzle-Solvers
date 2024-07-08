class Puzzle:
    """
    Represents the state of a sliding puzzle with any square matrix size (e.g. 3x3, 4x4...)
    """

    def __init__(self, position):
        self.position = position
        self.num_rows = len(position)
        self.num_columns = len(position[0])
        if self.num_rows != self.num_columns:
            raise RuntimeError('Invalid Puzzle dimensions')

    def __str__(self):
        puzzle_length = (3 * self.num_rows) + 1
        puzzle_string = '—' * puzzle_length + '\n'
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                puzzle_string += '│{0: >2}'.format(str(self.position[i][j]))
                if j == self.num_columns - 1:
                    puzzle_string += '│\n'
        puzzle_string += '—' * puzzle_length + '\n'
        return puzzle_string

    @staticmethod
    def generate_end_position(size):
        end_position = []
        new_row = []
        for i in range(1, size * size + 1):
            new_row.append(i)
            if len(new_row) == size:
                end_position.append(new_row)
                new_row = []
        end_position[-1][-1] = 0
        return end_position

    def find_tile_position(self, tile):
        for i, row in enumerate(self.position):
            for j, t in enumerate(row):
                if t == tile:
                    return i, j
        raise RuntimeError('Tile not found')

    def swap_tiles(self, x1, y1, x2, y2):
        puzzle_copy = [list(row) for row in self.position]
        puzzle_copy[x1][y1], puzzle_copy[x2][y2] = puzzle_copy[x2][y2], puzzle_copy[x1][y1]
        return puzzle_copy

    def find_empty_tile(self):
        return self.find_tile_position(0)

    def get_moves(self):
        moves = []
        i, j = self.find_empty_tile()
        if i > 0:
            moves.append(Puzzle(self.swap_tiles(i, j, i - 1, j)))  # move up
        if j < self.num_columns - 1:
            moves.append(Puzzle(self.swap_tiles(i, j, i, j + 1)))  # move right
        if j > 0:
            moves.append(Puzzle(self.swap_tiles(i, j, i, j - 1)))  # move left
        if i < self.num_rows - 1:
            moves.append(Puzzle(self.swap_tiles(i, j, i + 1, j)))  # move down
        return moves
