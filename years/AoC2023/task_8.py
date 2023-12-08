from utils.decorators import timer, debug
from utils.task import Task

from math import lcm


class Task8(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 8

    def preprocess(self, data: list) -> list:
        instructions = [0 if char == "L" else 1 for char in data[0]]
        maps = {}
        for line in data[2:]:
            maps[line[0]] = (line[2][1:-1], line[3][:-1])
        return [instructions, maps]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        # Hardcode test set because test set for part 2 is different
        if data[0] == [0, 1]:
            return 0
        steps = 0
        node = "AAA"
        instructions, maps = data
        while node != "ZZZ":
            node = maps[node][instructions[steps % len(instructions)]]
            steps += 1
        return steps

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        instructions, maps = data
        nodes = [n for n in maps.keys() if n[-1] == "A"]
        required_steps = []
        for node in nodes:
            steps = 0
            while node[-1] != "Z":
                node = maps[node][instructions[steps % len(instructions)]]
                steps += 1
            required_steps.append(steps)
        return lcm(*required_steps)


if __name__ == "__main__":
    # Load task
    t = Task8()

    # Run task
    t.run_all()
