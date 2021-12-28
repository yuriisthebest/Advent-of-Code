from utils.decorators import timer, debug
from utils.task import Task


class Task2(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 2

    def preprocess(self, data: list) -> list:
        test = []
        for line in data:
            test.append([line[0], int(line[1])])
        return test

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        distance = 0
        depth = 0
        for command in data:
            command, value = command
            if command == "forward":
                distance += value
            elif command == "down":
                depth += value
            elif command == "up":
                depth -= value
        return depth * distance

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        distance = 0
        depth = 0
        aim = 0
        for command in data:
            command, value = command
            if command == "forward":
                distance += value
                depth += value * aim
            elif command == "down":
                aim += value
            elif command == "up":
                aim -= value
        return depth * distance


if __name__ == "__main__":
    # Load task
    t = Task2()

    # Run task
    t.run_all()
