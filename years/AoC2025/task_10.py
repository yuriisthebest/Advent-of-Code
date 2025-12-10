from ortools.linear_solver import pywraplp
from itertools import combinations, combinations_with_replacement
from utils.decorators import timer, debug
from utils.task import Task


class Task10(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 10

    def preprocess(self, data: list) -> list:
        machines = []
        for line in data:
            lights = [char == "#" for char in line[0][1:-1]]
            joltage = [int(num) for num in line[-1][1:-1].split(",")]
            wiring = [tuple([int(num) for num in wire[1:-1].split(",")]) for wire in line[1:-1]]
            machines.append((lights, wiring, joltage))
        return machines

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        result = 0
        for machine in data:
            wanted_lights, wires, _ = machine
            result += self.fewest_presses(wanted_lights, wires)
        return result

    @staticmethod
    def fewest_presses(wanted_lights: list, wires: list) -> int:
        for i in range(len(wires)):
            # Determine all possible combinations of
            wire_combinations = combinations(wires, i + 1)
            for configuration in wire_combinations:
                lights = [False] * len(wanted_lights)
                for wire in configuration:
                    for num in wire:
                        lights[num] = lights[num] is False
                if lights == wanted_lights:
                    return i + 1
        return 0

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        result = 0
        for machine in data:
            _, wires, wanted_joltage = machine
            result += self.configure_joltage(wanted_joltage, wires)
        return result

    @staticmethod
    def configure_joltage(wanted_jolts: list, wires: list) -> int:
        # Determine which constraints a solution must follow
        constraints = []
        for i in range(len(wanted_jolts)):
            to_reach = wanted_jolts[i]
            needed = []
            for wire in wires:
                if i in wire:
                    needed.append(wire)
            constraints.append((needed, to_reach))

        # Use a integer solver
        solver = pywraplp.Solver.CreateSolver("SAT")
        # Setup variables (the wires)
        variables = [solver.IntVar(0, solver.infinity(), str(wire)) for wire in wires]
        # Setup optimization problem
        # Optimize the variables for the amount of button presses
        solver.Minimize(sum(variables))
        # Add jolt constraints
        for constraint in constraints:
            possible_wires, target = constraint
            possible_wires = [variables[wires.index(wire)] for wire in possible_wires]
            solver.Add(sum(possible_wires) == target)
        # Solve and return the number of required presses if a solution is found
        results = solver.Solve()
        if results == pywraplp.Solver.OPTIMAL:
            delta = 0.1
            return int(solver.Objective().Value() + delta)
        return 0


if __name__ == "__main__":
    # Load task
    t = Task10()

    # Run task
    t.run_all()
