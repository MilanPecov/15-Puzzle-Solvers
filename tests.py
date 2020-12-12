from main import PuzzleSolver, AStar, BreadthFirst, Puzzle


def test_generate_end_position():
    puzzle_4x4 = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])

    assert puzzle_4x4.PUZZLE_END_POSITION == [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], '4x4'

    puzzle_3x3 = Puzzle([[0, 2, 1], [3, 5, 4], [6, 7, 8], [9, 10, 11]])
    assert puzzle_3x3.PUZZLE_END_POSITION == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]], '3x3'


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


def test_all_possible_moves():
    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    output = puzzle.get_moves()

    assert output[0].position == [[1, 2, 0, 4], [5, 6, 3, 7], [8, 9, 10, 11], [12, 13, 14, 15]], 'up'
    assert output[1].position == [[1, 2, 3, 4], [5, 6, 7, 0], [8, 9, 10, 11], [12, 13, 14, 15]], 'right'
    assert output[2].position == [[1, 2, 3, 4], [5, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], 'left'
    assert output[3].position == [[1, 2, 3, 4], [5, 6, 10, 7], [8, 9, 0, 11], [12, 13, 14, 15]], 'down'


def test_heuristic_misplaced():
    puzzle = Puzzle([[1, 2, 0, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    misplaced = puzzle.heuristic_misplaced()

    assert misplaced == 3


def test_heuristic_manhattan_distance():
    puzzle = Puzzle([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])
    distance = puzzle.heuristic_manhattan_distance()

    assert distance == 16


def test_performance():
    puzzle_start = Puzzle([[4, 1, 2, 3], [5, 6, 7, 0], [8, 9, 10, 11], [12, 13, 14, 15]])

    s2 = PuzzleSolver(BreadthFirst(puzzle_start))
    s2.run()
    assert s2._strategy.num_expanded_nodes == 35

    s1 = PuzzleSolver(AStar(puzzle_start))
    s1.run()
    assert s1._strategy.num_expanded_nodes == 4


if __name__ == "__main__":
    test_generate_end_position()
    test_swap()
    test_get_coordinates()
    test_all_possible_moves()
    test_heuristic_misplaced()
    test_heuristic_manhattan_distance()
    test_performance()
    print("Everything passed")
