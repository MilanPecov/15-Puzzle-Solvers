import random

from fifteen_puzzle_solvers.domain import Puzzle
from fifteen_puzzle_solvers.services.puzzle.validation import PuzzleValidationService


class PuzzleShuffleService:
    """
    Provides services for shuffling puzzles.
    """

    @staticmethod
    def shuffle_puzzle(size):
        end_position = Puzzle.generate_end_position(size)
        while True:
            flat_list = [item for sublist in end_position for item in sublist]
            random.shuffle(flat_list)
            shuffled_position = [flat_list[i:i + size] for i in range(0, len(flat_list), size)]
            shuffled_puzzle = Puzzle(shuffled_position)
            if PuzzleValidationService.is_solvable(shuffled_puzzle):
                return shuffled_puzzle
