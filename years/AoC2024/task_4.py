from utils.decorators import timer, debug
from utils.task import Task


class Task4(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 4

    @staticmethod
    def check_position_xmas(data: list, i: int, j: int) -> list:
        if data[i][j] != "X":
            return []
        found = []
        for delta_y, delta_x in [(0, 1), (0, -1), (1, 1), (1, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1)]:
            for k, letter in enumerate("XMAS"):
                if i + k * delta_y < 0 or j + delta_x * k < 0:
                    break
                try:
                    data[i + delta_y * k][j + delta_x * k]
                except IndexError:
                    break
                if data[i + delta_y * k][j + delta_x * k] != letter:
                    break
            else:
                found.append((i, j, delta_y, delta_x))
        return found

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        total_found = 0
        for i, line in enumerate(data):
            for j, letter in enumerate(line):
                total_found += len(self.check_position_xmas(data, i, j))
        return total_found

    @staticmethod
    def check_position_mas(data: list, i: int, j: int) -> int:
        if data[i][j] != "A":
            return 0
        if i - 1 < 0 or j - 1 < 0:
            return 0
        if i + 1 >= len(data) or j + 1 >= len(data[0]):
            return 0
        # Check diagonal to right
        if not (data[i-1][j-1] in ["M", "S"] and data[i+1][j+1] in ["M", "S"] and data[i-1][j-1] != data[i+1][j+1]):
            return 0
        # Check diagonal to left
        if not (data[i+1][j-1] in ["M", "S"] and data[i-1][j+1] in ["M", "S"] and data[i+1][j-1] != data[i-1][j+1]):
            return 0
        return 1

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        total_found = 0
        for i, line in enumerate(data):
            for j, letter in enumerate(line):
                total_found += self.check_position_mas(data, i, j)
        return total_found


if __name__ == "__main__":
    # Load task
    t = Task4()

    # Run task
    t.run_all()
