from puzzle import Puzzle
from algorithms import AStar, BreadthFirst
from solver import PuzzleSolver


def test_generate_end_position():
    puzzle_4x4 = Puzzle([[0, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 1]])

    assert puzzle_4x4.PUZZLE_END_POSITION == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]], '4x4'

    puzzle_3x3 = Puzzle([[0, 2, 1], [3, 5, 4], [6, 7, 8]])
    assert puzzle_3x3.PUZZLE_END_POSITION == [[1, 2, 3], [4, 5, 6], [7, 8, 0]], '3x3'


def test_swap():
    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
    new_position = puzzle._swap(0, 0, 0, 1)

    assert new_position == [[2, 1, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


def test_get_coordinates():
    puzzle = Puzzle([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])
    i, j = puzzle._get_coordinates(0)

    assert i == 3
    assert j == 2

    i, j = puzzle._get_coordinates(10)
    assert i == 3
    assert j == 3


def test_generate_random_position():
    initial_position = [[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]]
    puzzle = Puzzle(initial_position.copy())
    puzzle.generate_random_position()
    new_position = puzzle.position

    assert initial_position != new_position


def test_all_possible_moves():
    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    output = puzzle.get_moves()

    assert output[0].position == [[1, 2, 0, 4], [5, 6, 3, 7], [8, 9, 10, 11], [12, 13, 14, 15]], 'up'
    assert output[1].position == [[1, 2, 3, 4], [5, 6, 7, 0], [8, 9, 10, 11], [12, 13, 14, 15]], 'right'
    assert output[2].position == [[1, 2, 3, 4], [5, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], 'left'
    assert output[3].position == [[1, 2, 3, 4], [5, 6, 10, 7], [8, 9, 0, 11], [12, 13, 14, 15]], 'down'


def test_heuristic_misplaced():
    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
    misplaced = puzzle.heuristic_misplaced()

    assert misplaced == 0

    puzzle = Puzzle([[1, 2, 4, 3], [5, 6, 8, 7], [9, 10, 12, 11], [13, 14, 15, 0]])
    misplaced = puzzle.heuristic_misplaced()
    assert misplaced == 6


def test_heuristic_manhattan_distance():
    puzzle = Puzzle([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])
    distance = puzzle.heuristic_manhattan_distance()

    assert distance == 28


def test_unsolvable_puzzle():
    puzzle = Puzzle([[1, 8, 2], [0, 4, 3], [7, 6, 5]])
    assert puzzle._get_inversions_count() == 10
    assert puzzle.is_solvable()

    puzzle = Puzzle([[13, 2, 10, 3], [1, 12, 8, 4], [5, 0, 9, 6], [15, 14, 11, 7]])
    assert puzzle._get_inversions_count() == 41
    assert puzzle.is_solvable()

    puzzle = Puzzle([[6, 13, 7, 10], [8, 9, 11, 0], [15, 2, 12, 5], [14, 3, 1, 4]])
    assert puzzle._get_inversions_count() == 62
    assert puzzle.is_solvable()

    puzzle = Puzzle([[3, 9, 1, 15], [14, 11, 4, 6], [13, 0, 10, 12], [2, 7, 8, 5]])
    assert puzzle._get_inversions_count() == 56
    assert not puzzle.is_solvable()

    puzzle = Puzzle([[1, 2, 3, 7], [12, 8, 15, 4], [13, 10, 11, 5], [9, 6, 14, 0]])
    assert puzzle._get_inversions_count() == 33
    assert not puzzle.is_solvable()


def test_performance():
    puzzle_start = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]])

    s2 = PuzzleSolver(BreadthFirst(puzzle_start))
    s2.run()
    assert s2._strategy.num_expanded_nodes == 56

    s1 = PuzzleSolver(AStar(puzzle_start))
    s1.run()
    s1.print_solution()
    assert s1._strategy.num_expanded_nodes == 4

    s1 = PuzzleSolver(AStar(puzzle_start, heuristic='misplaced'))
    s1.run()
    s1.print_solution()
    assert s1._strategy.num_expanded_nodes == 4


if __name__ == "__main__":
    test_generate_end_position()
    test_generate_random_position()
    test_swap()
    test_get_coordinates()
    test_all_possible_moves()
    test_heuristic_misplaced()
    test_heuristic_manhattan_distance()
    test_unsolvable_puzzle()
    test_performance()
    print("Everything passed")
