from fifteen_puzzle_solvers.domain.puzzle import Puzzle
from fifteen_puzzle_solvers.services.puzzle import PuzzleHeuristicService, PuzzleShuffleService, PuzzleValidationService
from fifteen_puzzle_solvers.services.algorithms import AStar, BreadthFirst
from fifteen_puzzle_solvers.services.solver import PuzzleSolver


def test_generate_end_position():
    end_position_4x4 = Puzzle.generate_end_position(4)
    assert end_position_4x4 == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12],
                                [13, 14, 15, 0]], "Failed to generate correct end position for 4x4 puzzle"

    end_position_3x3 = Puzzle.generate_end_position(3)
    assert end_position_3x3 == [[1, 2, 3], [4, 5, 6],
                                [7, 8, 0]], "Failed to generate correct end position for 3x3 puzzle"


def test_swap():
    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
    new_position = puzzle.swap_tiles(0, 0, 0, 1)
    assert new_position == [[2, 1, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12],
                            [13, 14, 15, 0]], "Failed to swap tiles correctly"


def test_get_coordinates():
    puzzle = Puzzle([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])
    i, j = puzzle.find_empty_tile()
    assert i == 3 and j == 2, f"Failed to find empty tile. Expected (3, 2), got ({i}, {j})"

    i, j = puzzle.find_tile_position(10)
    assert i == 3 and j == 3, f"Failed to find tile 10. Expected (3, 3), got ({i}, {j})"


def test_generate_random_position():
    size = 4
    end_position = Puzzle.generate_end_position(size)
    shuffled_puzzle = PuzzleShuffleService.shuffle_puzzle(size)

    assert shuffled_puzzle.position != end_position, "The shuffled puzzle should be different from the end position"
    assert PuzzleValidationService.is_solvable(shuffled_puzzle), "The shuffled puzzle should be solvable"


def test_all_possible_moves():
    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    output = puzzle.get_moves()

    assert output[0].position == [[1, 2, 0, 4], [5, 6, 3, 7], [8, 9, 10, 11],
                                  [12, 13, 14, 15]], "Failed to move tile up correctly"
    assert output[1].position == [[1, 2, 3, 4], [5, 6, 7, 0], [8, 9, 10, 11],
                                  [12, 13, 14, 15]], "Failed to move tile right correctly"
    assert output[2].position == [[1, 2, 3, 4], [5, 0, 6, 7], [8, 9, 10, 11],
                                  [12, 13, 14, 15]], "Failed to move tile left correctly"
    assert output[3].position == [[1, 2, 3, 4], [5, 6, 10, 7], [8, 9, 0, 11],
                                  [12, 13, 14, 15]], "Failed to move tile down correctly"


def test_heuristic_misplaced():
    end_position = Puzzle.generate_end_position(4)

    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
    misplaced = PuzzleHeuristicService(end_position).heuristic_misplaced(puzzle.position)
    assert misplaced == 0, f"Expected 0 misplaced tiles, got {misplaced}"

    puzzle = Puzzle([[1, 2, 4, 3], [5, 6, 8, 7], [9, 10, 12, 11], [13, 14, 15, 0]])
    misplaced = PuzzleHeuristicService(end_position).heuristic_misplaced(puzzle.position)
    assert misplaced == 6, f"Expected 6 misplaced tiles, got {misplaced}"


def test_heuristic_manhattan_distance():
    end_position = Puzzle.generate_end_position(4)

    puzzle = Puzzle([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])
    distance = PuzzleHeuristicService(end_position).heuristic_manhattan_distance(puzzle.position)
    assert distance == 27, f"Expected Manhattan distance of 27, got {distance}"


def test_unsolvable_puzzle():
    puzzle = Puzzle([[1, 8, 2], [0, 4, 3], [7, 6, 5]])
    assert PuzzleValidationService._get_inversions_count(puzzle.position) == 10, "Expected 10 inversions"
    assert PuzzleValidationService.is_solvable(puzzle), "Expected puzzle to be solvable"

    puzzle = Puzzle([[13, 2, 10, 3], [1, 12, 8, 4], [5, 0, 9, 6], [15, 14, 11, 7]])
    assert PuzzleValidationService._get_inversions_count(puzzle.position) == 41, "Expected 41 inversions"
    assert PuzzleValidationService.is_solvable(puzzle), "Expected puzzle to be solvable"

    puzzle = Puzzle([[6, 13, 7, 10], [8, 9, 11, 0], [15, 2, 12, 5], [14, 3, 1, 4]])
    assert PuzzleValidationService._get_inversions_count(puzzle.position) == 62, "Expected 62 inversions"
    assert PuzzleValidationService.is_solvable(puzzle), "Expected puzzle to be solvable"

    puzzle = Puzzle([[3, 9, 1, 15], [14, 11, 4, 6], [13, 0, 10, 12], [2, 7, 8, 5]])
    assert PuzzleValidationService._get_inversions_count(puzzle.position) == 56, "Expected 56 inversions"
    assert not PuzzleValidationService.is_solvable(puzzle), "Expected puzzle to be unsolvable"

    puzzle = Puzzle([[1, 2, 3, 7], [12, 8, 15, 4], [13, 10, 11, 5], [9, 6, 14, 0]])
    assert PuzzleValidationService._get_inversions_count(puzzle.position) == 33, "Expected 33 inversions"
    assert not PuzzleValidationService.is_solvable(puzzle), "Expected puzzle to be unsolvable"


def test_performance_low_complexity():
    puzzle_start = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]])

    s2 = PuzzleSolver(BreadthFirst(puzzle_start))
    s2.run()
    assert s2.get_num_expanded_nodes() == 56, f"Expected 56 expanded nodes for BreadthFirst, got {s2.get_num_expanded_nodes()}"

    s1 = PuzzleSolver(AStar(puzzle_start))
    s1.run()
    s1.print_solution()
    assert s1.get_num_expanded_nodes() == 4, f"Expected 4 expanded nodes for A* with default heuristic, got {s1.get_num_expanded_nodes()}"

    s1 = PuzzleSolver(AStar(puzzle_start, heuristic='misplaced'))
    s1.run()
    s1.print_solution()
    assert s1.get_num_expanded_nodes() == 4, f"Expected 4 expanded nodes for A* with misplaced heuristic, got {s1.get_num_expanded_nodes()}"


def test_performance_mid_complexity():
    puzzle_start = Puzzle([[1, 14, 3, 12], [8, 10, 11, 7], [9, 0, 5, 4], [15, 6, 13, 2]])
    s1 = PuzzleSolver(AStar(puzzle_start))
    s1.run()
    s1.print_solution()
    assert s1.get_num_expanded_nodes() == 277, f"Expected 277 expanded nodes for A* with mid complexity, got {s1.get_num_expanded_nodes()}"


def test_performance_high_complexity():
    puzzle_start = Puzzle([[7, 10, 3, 4], [14, 0, 12, 8], [9, 2, 15, 6], [13, 5, 1, 11]])
    s1 = PuzzleSolver(AStar(puzzle_start))
    s1.run()
    s1.print_solution()
    assert s1.get_num_expanded_nodes() == 873, f"Expected 873 expanded nodes for A* with high complexity, got {s1.get_num_expanded_nodes()}"


if __name__ == "__main__":
    test_generate_end_position()
    test_generate_random_position()
    test_swap()
    test_get_coordinates()
    test_all_possible_moves()
    test_heuristic_misplaced()
    test_heuristic_manhattan_distance()
    test_unsolvable_puzzle()
    test_performance_low_complexity()
    test_performance_mid_complexity()
    test_performance_high_complexity()
    print("Everything passed")
