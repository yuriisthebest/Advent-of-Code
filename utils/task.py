from utils.decorators import timer, debug
from utils import load
from abc import abstractmethod


class Task:
    # Task constants
    YEAR = 2021
    TASK_NUM = 2
    TEST_MODE = False
    IS_TEST = False

    def load(self) -> tuple:
        test, task = load.load_task_txt(self.YEAR, self.TASK_NUM)
        test = self.preprocess(test)
        task = self.preprocess(task)
        return test, task

    def preprocess(self, data: list) -> list:
        return data

    @abstractmethod
    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        return len(data)

    @abstractmethod
    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        return len(data)

    def __init__(self):
        self.test, self.task = self.load()

    def run_part_1(self):
        # Run part 1
        self.IS_TEST = True
        test1 = self.part_1(self.test)
        self.IS_TEST = False
        task1 = self.part_1(self.task) if not self.TEST_MODE else None
        return test1, task1

    def run_part_2(self):
        # Run part 2
        self.IS_TEST = True
        test2 = self.part_2(self.test)
        self.IS_TEST = False
        task2 = self.part_2(self.task) if not self.TEST_MODE else None
        return test2, task2

    def run_all(self):
        res1 = self.run_part_1()
        self.test, self.task = self.load()
        res2 = self.run_part_2()
        return res1, res2


if __name__ == "__main__":
    # Load task
    t = Task()

    # Run part 1
    t.run_part_1()
    # Run part 2
    t.run_part_2()
