from utils.decorators import timer, debug
from utils.task import Task


class TaskT(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 1

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
    t = TaskT()

    # Run task
    t.run_all()
