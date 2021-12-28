from utils.decorators import timer, debug
from utils.task import Task
from utils.load import load_task_json


class Task1(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 1

    def load(self) -> tuple:
        test, task = load_task_json(self.YEAR, self.TASK_NUM)
        return test, task

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        """
        Count the number of times a measurement (element in list) increases from the previous measurement

        :param data: List of numbers
        :return: Number of measurements that are larger than the previous measurement
        """
        num_increases = 0
        for i, num in enumerate(data):
            if i == len(data) - 1:
                continue
            if num < data[i + 1]:
                num_increases += 1
        return num_increases

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Count the number of times the sum of a three-sliding window increases from the previous sum

        :param data: List of numbers
        :return: Number of sums larger than the previous sum
        """
        num_increases = 0
        for i, num in enumerate(data):
            if i == len(data) - 3:
                break
            sum1 = num + data[i + 1] + data[i + 2]
            sum2 = sum1 - num + data[i + 3]
            if sum2 > sum1:
                num_increases += 1
        return num_increases


if __name__ == "__main__":
    # Load task
    t = Task1()

    # Run task
    t.run_all()
