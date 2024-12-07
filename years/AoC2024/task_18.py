from utils.decorators import timer, debug
from utils.task import Task


class Task18(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 18

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
    t = Task18()

    # Run task
    t.run_all()
