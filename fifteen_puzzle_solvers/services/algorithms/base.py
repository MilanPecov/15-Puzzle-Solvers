from abc import ABC, abstractmethod


class IStrategy(ABC):
    num_expanded_nodes = 0
    solution = None

    @abstractmethod
    def solve_puzzle(self):
        raise NotImplementedError
