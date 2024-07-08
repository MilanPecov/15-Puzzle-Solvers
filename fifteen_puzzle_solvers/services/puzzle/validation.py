from fifteen_puzzle_solvers.domain import Puzzle


class PuzzleValidationService:
    """
    Provides services for validating puzzle solvability.
    """

    @classmethod
    def is_solvable(cls, puzzle: Puzzle):
        size = puzzle.num_rows
        inversions_count = cls._get_inversions_count(puzzle.position)
        blank_position = cls._get_blank_space_row_from_bottom(puzzle)
        if size % 2 != 0 and inversions_count % 2 == 0:
            return True
        elif size % 2 == 0 and ((blank_position % 2 == 0 and inversions_count % 2 != 0) or (
                blank_position % 2 != 0 and inversions_count % 2 == 0)):
            return True
        return False

    @staticmethod
    def _get_inversions_count(position):
        inv_count = 0
        puzzle_list = [number for row in position for number in row if number != 0]
        for i in range(len(puzzle_list)):
            for j in range(i + 1, len(puzzle_list)):
                if puzzle_list[i] > puzzle_list[j]:
                    inv_count += 1
        return inv_count

    @classmethod
    def _get_blank_space_row_from_bottom(cls, puzzle: Puzzle):
        zero_row, _ = puzzle.find_empty_tile()
        return puzzle.num_rows - zero_row
