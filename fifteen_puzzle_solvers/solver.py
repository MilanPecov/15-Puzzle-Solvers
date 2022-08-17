class PuzzleSolver:
    """
    Executes different puzzle solver strategies and prints their performance
    """

    def __init__(self, strategy):
        """
        :param strategy: Strategy
        """
        self._strategy = strategy

    def print_performance(self):
        print(f'{self._strategy} - Expanded Nodes: {self._strategy.num_expanded_nodes}')

    def print_solution(self):
        print('Solution:')
        for s in self._strategy.solution:
            print(s)

    def run(self):
        if not self._strategy.start.is_solvable():
            raise RuntimeError('This puzzle is not solvable')

        self._strategy.do_algorithm()
