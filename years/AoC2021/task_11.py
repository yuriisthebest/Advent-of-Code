from utils.decorators import timer, debug
from utils.task import Task


class Task11(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 11

    def preprocess(self, data: list) -> list:
        data = [[int(value) for value in row] for row in data]
        return data

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list, max_steps: int = 100) -> int:
        data = data.copy()
        flashes = 0
        for step in range(max_steps):
            flashed = []
            must_increase = [(i, j) for i in range(10) for j in range(10)]
            while len(must_increase) != 0:
                x, y = must_increase.pop(0)
                data[x][y] = (data[x][y] + 1) % 10
                # Flash the octopus if the value if higher than 9, aka just turned 0
                if data[x][y] == 0 and (x, y) not in flashed:
                    flashes += 1
                    flashed.append((x, y))
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if x+i < 0 or x+i > 9:
                                continue
                            if y+j < 0 or y+j > 9:
                                continue
                            must_increase.append((x+i, y+j))
            # Reset flashed octopuses
            for x, y in flashed:
                data[x][y] = 0
            # Print board
            if step < 2 and False:
                print(f"After step {step+1}:")
                x = ["".join([str(val) for val in row]) for row in data]
                for row in x:
                    print(row)
                print()
        return flashes

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        data = data.copy()
        flashes = 0
        step = 0
        flashed = []
        while len(flashed) != 100:
            step += 1
            flashed = []
            must_increase = [(i, j) for i in range(10) for j in range(10)]
            while len(must_increase) != 0:
                x, y = must_increase.pop(0)
                data[x][y] = (data[x][y] + 1) % 10
                # Flash the octopus if the value if higher than 9, aka just turned 0
                if data[x][y] == 0 and (x, y) not in flashed:
                    flashes += 1
                    flashed.append((x, y))
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if x + i < 0 or x + i > 9:
                                continue
                            if y + j < 0 or y + j > 9:
                                continue
                            must_increase.append((x + i, y + j))
            # Reset flashed octopuses
            for x, y in flashed:
                data[x][y] = 0
            # Print board
            if step < 3 and False:
                print(f"After step {step}:")
                x = ["".join([str(val) for val in row]) for row in data]
                for row in x:
                    print(row)
                print()
        return step


if __name__ == "__main__":
    # Load task
    t = Task11()

    # Run task
    t.run_all()
