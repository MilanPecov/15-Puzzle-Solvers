class PuzzleSolver:
    """
    Executes different puzzle solver strategies (algorithms) and prints the solution and the performance
    """

    def __init__(self, strategy):
        """
        :param strategy: Strategy
        """
        self._strategy = strategy

    def print_performance(self):
        """
        Number of expanded nodes in the search tree
        """
        print(f'{self._strategy} - Expanded Nodes: {self._strategy.num_expanded_nodes}')

    def print_solution(self):
        """
        Explanation how to solve the puzzle
        """
        print('Solution:')
        for s in self._strategy.solution:
            print(s)

    def run(self):
        if not self._strategy.start.is_solvable():  # check if the puzzle is solvable before running the algorithm
            raise RuntimeError('This puzzle is not solvable')

        self._strategy.solve_puzzle()
