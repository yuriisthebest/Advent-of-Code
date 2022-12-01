from utils.decorators import timer, debug
from utils.task import Task


class Task1(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 1

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        """
        Find the elf who carries the most calories

        :param data: List of numbers with empty spaces between individual elfs
        :return: Maximum amount of calories an elf is carrying
        """
        data.append('')
        max_sum = 0
        total = 0
        for i, num in enumerate(data):
            if num == "":
                max_sum = max(max_sum, total)
                total = 0
            else:
                total += int(num)
        return max_sum

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Find the top three elfs who carry the most calories

        :param data: List of numbers with empty spaces between individual elfs
        :return: Sum of the top three calories the elfs are carrying
        """
        data.append('')
        sums = []
        total = 0
        for i, num in enumerate(data):
            if num == "":
                sums.append(total)
                total = 0
            else:
                total += int(num)
        sums.sort(reverse=True)
        return sum(sums[:3])


if __name__ == "__main__":
    # Load task
    t = Task1()

    # Run task
    t.run_all()
