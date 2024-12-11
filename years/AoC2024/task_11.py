from functools import cache
from utils.decorators import timer, debug
from utils.task import Task


class Task11(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 11

    def preprocess(self, data: list) -> list:
        return [int(num) for num in data[0]]

    @staticmethod
    def blink(stones: list) -> list:
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                new_stones.append(int(str(stone)[:len(str(stone)) // 2]))
                new_stones.append(int(str(stone)[len(str(stone)) // 2:]))
            else:
                new_stones.append(stone * 2024)
        return new_stones

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        for i in range(25):
            data = self.blink(data)
        return len(data)

    @cache
    def num_splits(self, num: int, times: int) -> int:
        # How often does this num split
        if times == 0:
            return 1
        if num == 0:
            return self.num_splits(1, times - 1)
        if len(str(num)) % 2 == 0:
            return self.num_splits(int(str(num)[:len(str(num)) // 2]), times - 1) + self.num_splits(int(str(num)[len(str(num)) // 2:]), times - 1)
        else:
            return self.num_splits(num * 2024, times - 1)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        total = 0
        for num in data:
            total += self.num_splits(num, 75)
        return total


if __name__ == "__main__":
    # Load task
    t = Task11()

    # Run task
    t.run_all()
