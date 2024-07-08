class PuzzleHeuristicService:
    """
    Provides services for calculating puzzle heuristics.
    """

    def __init__(self, end_position):
        self.end_position = end_position

    def heuristic_misplaced(self, position):
        misplaced = 0
        for i in range(len(position)):
            for j in range(len(position[0])):
                if position[i][j] != self.end_position[i][j]:
                    misplaced += 1
        return misplaced

    def heuristic_manhattan_distance(self, position):
        distance = 0
        size = len(position)
        for i in range(size):
            for j in range(size):
                tile = position[i][j]
                if tile != 0:
                    target_row = (tile - 1) // size
                    target_col = (tile - 1) % size
                    distance += abs(i - target_row) + abs(j - target_col)
        return distance

    @staticmethod
    def heuristic_linear_conflict(position):
        conflict = 0
        size = len(position)

        # Row conflicts
        for row in range(size):
            max_val = -1
            for col in range(size):
                value = position[row][col]
                if value != 0 and (value - 1) // size == row:
                    if value > max_val:
                        max_val = value
                    else:
                        conflict += 2

        # Column conflicts
        for col in range(size):
            max_val = -1
            for row in range(size):
                value = position[row][col]
                if value != 0 and (value - 1) % size == col:
                    if value > max_val:
                        max_val = value
                    else:
                        conflict += 2

        return conflict

    @staticmethod
    def heuristic_walking_distance(position):
        # Create a grid to store the walking distances
        size = len(position)
        distance_grid = [[0] * size for _ in range(size)]

        for row in range(size):
            for col in range(size):
                value = position[row][col]
                if value != 0:
                    target_row = (value - 1) // size
                    target_col = (value - 1) % size
                    distance_grid[row][col] = abs(row - target_row) + abs(col - target_col)

        # Calculate the walking distance
        walking_distance = 0
        for row in range(size):
            for col in range(size):
                walking_distance += distance_grid[row][col]

        return walking_distance

    def heuristic_total(self, position):
        return (self.heuristic_manhattan_distance(position) +
                self.heuristic_linear_conflict(position) +
                self.heuristic_walking_distance(position))
