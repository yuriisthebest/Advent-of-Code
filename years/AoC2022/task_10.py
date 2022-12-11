from utils.decorators import timer, debug
from utils.task import Task


class Task10(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 10

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        register = 1
        cycle = 0
        signal_strengths = 0
        for instruction in data:
            iterator = 2 if instruction[0] == "addx" else 1
            for _ in range(iterator):
                cycle += 1
                if cycle % 40 == 20:
                    signal_strengths += cycle * register
            if instruction[0] == "addx":
                register += int(instruction[1])
        return signal_strengths

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        result = ""
        register = 1
        cycle = 0
        signal_strengths = 0
        for instruction in data:
            iterator = 2 if instruction[0] == "addx" else 1
            for _ in range(iterator):
                cycle += 1
                if abs(((cycle-1) % 40) - register) <= 1:
                    result += "#"
                else:
                    result += " "
                if cycle % 40 == 0:
                    result += "\n"
                # To compute part 1
                if cycle % 40 == 20:
                    signal_strengths += cycle * register
            if instruction[0] == "addx":
                register += int(instruction[1])
        print(result)
        return signal_strengths


if __name__ == "__main__":
    # Load task
    t = Task10()

    # Run task
    t.run_all()
