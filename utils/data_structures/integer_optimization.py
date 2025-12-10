from typing import Any, Callable


class IntegerOptimization:
    def __init__(self, strategy: str = "default"):
        self.strategy = strategy
        self.objective = None
        self.objective_type = None

    def minimize(self, objective: Callable):
        self.objective = objective
        self.objective_type = "minimize"

    def maximize(self, objective: Callable):
        self.objective = objective
        self.objective_type = "maximize"

    def add_constraint(self, check):
        # The check is something like "function with variables" == | > | < "target". Parse and process this
        pass

    def solve(self):
        pass
