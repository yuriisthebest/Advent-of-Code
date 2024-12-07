from utils.decorators import timer, debug
from utils.task import Task


class Task1(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 1

    def preprocess(self, data: list) -> list:
        left_locations = []
        right_locations = []
        for line in data:
            left_locations.append(int(line[0]))
            right_locations.append(int(line[3]))
        return [left_locations, right_locations]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list[list, list]) -> int:
        left = data[0]
        left.sort()
        right = data[1]
        right.sort()
        total = 0
        for left_num, right_num in zip(left, right):
            total += abs(left_num - right_num)
        return total

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list[list, list]) -> int:
        left = data[0]
        right = data[1]
        total = 0
        for left_num in left:
            total += left_num * right.count(left_num)
        return total


if __name__ == "__main__":
    # Load task
    t = Task1()

    # Run task
    t.run_all()
