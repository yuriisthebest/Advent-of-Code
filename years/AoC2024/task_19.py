from functools import cache
from utils.decorators import timer, debug
from utils.task import Task


class Task19(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 19

    @cache
    def count_designs(self, patterns: list, design: str) -> int:
        if design == "":
            return 1
        num_designs = 0
        for pat in patterns:
            if design[:len(pat)] == pat:
                num_designs += self.count_designs(patterns, design[len(pat):])
        return num_designs

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        num_solved = 0
        patterns = tuple([pat[:-1] if pat[-1] == "," else pat for pat in data[0]])
        for design in data[2:]:
            if self.count_designs(patterns, design) > 0:
                num_solved += 1
        return num_solved

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        num_solved = 0
        patterns = tuple([pat[:-1] if pat[-1] == "," else pat for pat in data[0]])
        for design in data[2:]:
            num_solved += self.count_designs(patterns, design)
        return num_solved


if __name__ == "__main__":
    # Load task
    t = Task19()

    # Run task
    t.run_all()
