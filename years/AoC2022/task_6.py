from utils.decorators import timer, debug
from utils.task import Task


class Task6(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 6

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list, distinct_chars: int = 4) -> int:
        solution = 0
        for datastream in data:
            for i in range(len(datastream)):
                if len(set(datastream[i:i + distinct_chars])) == distinct_chars:
                    solution += i + distinct_chars
                    break
        return solution

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        return self.part_1(data, 14)


if __name__ == "__main__":
    # Load task
    t = Task6()

    # Run task
    t.run_all()
