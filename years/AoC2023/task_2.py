from utils.decorators import timer, debug
from utils.task import Task


class Task2(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 2

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        result = 0
        maximum = {'red': 12, 'green': 13, 'blue': 14}
        for line in data:
            line[-1] += ";"
            game_id = int(line[1][:-1])
            # Check every number-color pair in input
            for i, num in enumerate(line):
                if not num.isnumeric() or i < 2:
                    continue
                num = int(num)
                # Check if game is impossible
                if maximum[line[i+1][:-1]] < num:
                    break
            else:
                result += game_id
        return result

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        result = 0
        for line in data:
            # Keep track of minimum required boxes of each color (equal to maximum value found of each color)
            maximum = {'red': 0, 'green': 0, 'blue': 0}
            line[-1] += ";"
            # Check every number-color pair in input
            for i, num in enumerate(line):
                if not num.isnumeric() or i < 2:
                    continue
                num = int(num)
                # Check if game is impossible
                if maximum[line[i + 1][:-1]] < num:
                    maximum[line[i + 1][:-1]] = num
            # Calculate power of game
            game_result = 1
            for num in maximum.values():
                game_result *= num
            result += game_result
        return result


if __name__ == "__main__":
    # Load task
    t = Task2()

    # Run task
    t.run_all()
