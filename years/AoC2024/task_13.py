from ortools.linear_solver import pywraplp

from utils.decorators import timer, debug
from utils.task import Task


class Task13(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 13

    def preprocess(self, data: list) -> list:
        games = []
        new_game = []
        data.append("")
        for line in data:
            if line == "":
                games.append(new_game)
                new_game = []
            elif line[0] == "Button":
                x_button = int(line[2][2:-1])
                y_button = int(line[3][2:])
                new_game.append((x_button, y_button))
            else:
                x_button = int(line[1][2:-1])
                y_button = int(line[2][2:])
                new_game.append((x_button, y_button))
        return games

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        tokens = 0
        for game in data:
            tokens += self.solve_mathematically(game)
        return tokens

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        added = 10000000000000
        tokens = 0
        for game in data:
            game[2] = (game[2][0] + added, game[2][1] + added)
            tokens += self.solve_mathematically(game)
        return tokens

    @staticmethod
    def solve_mathematically(game: list) -> int:
        button_a, button_b, target = game
        solver = pywraplp.Solver.CreateSolver("GLOP")
        # Setup variables
        x = solver.IntVar(0, solver.infinity(), "x")
        y = solver.IntVar(0, solver.infinity(), "y")
        # Setup optimization problem
        # Optimize x and y for: goal = A * x + B * y
        solver.Minimize(3 * x + 1 * y)
        solver.Add(x * button_a[0] + y * button_b[0] == target[0])
        solver.Add(x * button_a[1] + y * button_b[1] == target[1])
        # Solve and return the number of required tokens if a solution is found
        results = solver.Solve()
        if results == pywraplp.Solver.OPTIMAL:
            delta = 0.1
            if all([int(x.solution_value() + delta) * button_a[i]
                    + int(y.solution_value() + delta) * button_b[i]
                    == target[i] for i in [0, 1]]):
                return int(solver.Objective().Value() + delta)
        return 0


if __name__ == "__main__":
    # Load task
    t = Task13()

    # Run task
    t.run_all()
