from main import Strategy, PuzzleSolver, AStar, BreadthFirst


def test_swap():
    puzzle = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    s = Strategy()
    new_position = s._swap(puzzle, 0, 0, 0, 1)

    assert new_position == [[2, 1, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


def test_get_blank_space_coordinates():
    puzzle = [[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]]
    s = Strategy()
    i, j = s._get_blank_space_coordinates(puzzle)

    assert i == 3
    assert j == 2


def test_all_possible_moves():
    puzzle = ((1, 2, 3, 4), (5, 6, 0, 7), (8, 9, 10, 11), (12, 13, 14, 15))
    s = Strategy()
    output = s._get_moves(puzzle)

    assert output[0] == [[1, 2, 0, 4], [5, 6, 3, 7], [8, 9, 10, 11], [12, 13, 14, 15]], 'up'
    assert output[1] == [[1, 2, 3, 4], [5, 6, 7, 0], [8, 9, 10, 11], [12, 13, 14, 15]], 'right'
    assert output[2] == [[1, 2, 3, 4], [5, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], 'left'
    assert output[3] == [[1, 2, 3, 4], [5, 6, 10, 7], [8, 9, 0, 11], [12, 13, 14, 15]], 'down'


def test_performance():
    puzzle_start = ((4, 1, 2, 3), (5, 6, 7, 0), (8, 9, 10, 11), (12, 13, 14, 15))

    s1 = PuzzleSolver(AStar(puzzle_start))
    s1.run()
    assert s1._strategy.num_expanded_nodes == 4

    s2 = PuzzleSolver(BreadthFirst(puzzle_start))
    s2.run()
    assert s2._strategy.num_expanded_nodes == 35


if __name__ == "__main__":
    test_swap()
    test_get_blank_space_coordinates()
    test_all_possible_moves()
    test_performance()
    print("Everything passed")
