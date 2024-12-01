from utils.decorators import timer, debug
from utils.task import Task


class Task14(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 14

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        return len(data)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        return len(data)


if __name__ == "__main__":
    # Load task
    t = Task14()

    # Run task
    t.run_all()
