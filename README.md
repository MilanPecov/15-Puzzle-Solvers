# Introduction

The 15-puzzle is a sliding puzzle that consists of a frame of numbered
square tiles in random order with one tile missing.
The puzzle also exists in other sizes, particularly the smaller 8-puzzle.
If the size is 3x3 tiles, the puzzle is called the 8-puzzle or 9-puzzle, and
if 4x4 tiles, the puzzle is called the 15-puzzle or 16-puzzle named,
respectively, for the number of tiles and the number of spaces.

The object of the puzzle is to place the tiles in order by making sliding
moves that use the empty space.

The n-puzzle is a classical problem for modelling algorithms involving
heuristics.

![Alt text](puzzle.jpg)


# Installation
```
pip install fifteen-puzzle-solvers
```

# Running the puzzle solvers

This code implements two different puzzle solvers
* Bread First Algorithm
* A* Algorithm
  * Heuristic 1: counting the number of misplaces tiles
  * Heuristic 2: finding the sum of the Manhattan distances between each block
      and its position in the goal configuration

```
from fifteen_puzzle_solvers.puzzle import Puzzle
from fifteen_puzzle_solvers.algorithms import AStar, BreadthFirst
from fifteen_puzzle_solvers.solver import PuzzleSolver

puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]])

for strategy in [BreadthFirst, AStar]:
    puzzle_solver = PuzzleSolver(strategy(puzzle))
    puzzle_solver.run()
    puzzle_solver.print_performance()
    puzzle_solver.print_solution()
```

Output
```
Breadth First - Expanded Nodes: 56
Solution:
—————————————
│ 1│ 2│ 3│ 4│
│ 5│ 6│ 7│ 8│
│ 0│10│11│12│
│ 9│13│14│15│
—————————————
—————————————
│ 1│ 2│ 3│ 4│
│ 5│ 6│ 7│ 8│
│ 9│10│11│12│
│ 0│13│14│15│
—————————————
—————————————
│ 1│ 2│ 3│ 4│
│ 5│ 6│ 7│ 8│
│ 9│10│11│12│
│13│ 0│14│15│
—————————————
—————————————
│ 1│ 2│ 3│ 4│
│ 5│ 6│ 7│ 8│
│ 9│10│11│12│
│13│14│ 0│15│
—————————————
—————————————
│ 1│ 2│ 3│ 4│
│ 5│ 6│ 7│ 8│
│ 9│10│11│12│
│13│14│15│ 0│
—————————————

A* - Expanded Nodes: 4
Solution:
—————————————
│ 1│ 2│ 3│ 4│
│ 5│ 6│ 7│ 8│
│ 0│10│11│12│
│ 9│13│14│15│
—————————————
—————————————
│ 1│ 2│ 3│ 4│
│ 5│ 6│ 7│ 8│
│ 9│10│11│12│
│ 0│13│14│15│
—————————————
—————————————
│ 1│ 2│ 3│ 4│
│ 5│ 6│ 7│ 8│
│ 9│10│11│12│
│13│ 0│14│15│
—————————————
—————————————
│ 1│ 2│ 3│ 4│
│ 5│ 6│ 7│ 8│
│ 9│10│11│12│
│13│14│ 0│15│
—————————————
—————————————
│ 1│ 2│ 3│ 4│
│ 5│ 6│ 7│ 8│
│ 9│10│11│12│
│13│14│15│ 0│
—————————————
```

# Testing different A* heuristic functions
```
from fifteen_puzzle_solvers.puzzle import Puzzle
from fifteen_puzzle_solvers.algorithms import AStar
from fifteen_puzzle_solvers.solver import PuzzleSolver

puzzle = Puzzle([[0, 1, 2], [3, 4, 5], [6, 7, 8]])  # 3x3 puzzle
puzzle.generate_random_position()

puzzle_solver = PuzzleSolver(AStar(puzzle, heuristic='misplaced'))
puzzle_solver.run()
puzzle_solver.print_performance()

>> Output: A* - Expanded Nodes: 979

puzzle_solver = PuzzleSolver(AStar(puzzle, heuristic='manhattan_distance'))  # default heuristic
puzzle_solver.run()
puzzle_solver.print_performance()

>> Output: A* - Expanded Nodes: 180
```