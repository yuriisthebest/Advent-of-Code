from utils.decorators import timer, debug
from utils import load

# Task constants
YEAR = 2021
TASK_NUM = 0


@debug
@timer(YEAR, TASK_NUM)
def part_1(data: list) -> int:
    return len(data)


@debug
@timer(YEAR, TASK_NUM)
def part_2(data: list) -> int:
    return len(data)


if __name__ == "__main__":
    # Load datasets
    test, task = load.load_task_txt(YEAR, TASK_NUM)

    # Run part 1
    part_1(test)
    part_1(task)
    # Run part 2
    part_2(test)
    part_2(task)
