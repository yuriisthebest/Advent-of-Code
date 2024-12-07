import re

from utils.decorators import timer, debug
from utils.task import Task


class Task3(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 3

    def preprocess(self, data: list) -> str:
        in_one_list = [part for line in data for part in line] if len(data) > 1 else data
        return "".join(in_one_list)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: str) -> int:
        total = 0
        matches = re.findall(r'mul\((\d+),(\d+)\)', data)
        for match in matches:
            total += int(match[0]) * int(match[1])
        return total

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: str) -> int:
        return self.calculate_score(data)

    def calculate_score(self, memory: str, do: bool = True):
        if do:
            next_mul = re.search(r'mul\((\d+),(\d+)\)', memory)
            next_dont = re.search(r"don't\(\)", memory)
            if next_mul is None:
                return 0
            if next_dont is not None and next_dont.start() < next_mul.start():
                return self.calculate_score(memory[next_dont.end():], False)
            score = int(next_mul.groups()[0]) * int(next_mul.groups()[1])
            return self.calculate_score(memory[next_mul.end():], True) + score
        else:
            next_do = re.search(r'do\(\)', memory)
            if next_do is None:
                return 0
            return self.calculate_score(memory[next_do.end():], True)


if __name__ == "__main__":
    # Load task
    t = Task3()

    # Run task
    t.run_all()
