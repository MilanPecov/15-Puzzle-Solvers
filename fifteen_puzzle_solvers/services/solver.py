from fifteen_puzzle_solvers.services import PuzzleValidationService


class PuzzleSolver:
    """
    Executes different puzzle solver strategies (algorithms) and prints the solution and the performance
    """

    def __init__(self, strategy):
        self._strategy = strategy
        self.puzzle_validation_service = PuzzleValidationService()

    def run(self):
        if not self.puzzle_validation_service.is_solvable(self._strategy.start):
            raise RuntimeError('This puzzle is not solvable')
        self._strategy.solve_puzzle()

    def print_performance(self):
        print(f'{self._strategy} - Expanded Nodes: {self.get_num_expanded_nodes()}')

    def print_solution(self):
        print('Solution:')
        for s in self._strategy.solution:
            print(s)

    def get_num_expanded_nodes(self):
        return self._strategy.num_expanded_nodes

    def get_solution(self):
        return self._strategy.solution
