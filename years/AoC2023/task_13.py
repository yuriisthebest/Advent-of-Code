from utils.decorators import timer, debug
from utils.task import Task

import copy


class Task13(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 13

    def preprocess(self, data: list) -> list:
        patterns = []
        current = {"rows": [], "columns": ["" for _ in range(20)]}
        for line in data:
            if line == "":
                current["columns"] = [x for x in current["columns"] if x != ""]
                patterns.append(current)
                current = {"rows": [], "columns": ["" for _ in range(20)]}
            else:
                current["rows"].append(line)
                for i, char in enumerate(line):
                    current["columns"][i] += char
        current["columns"] = [x for x in current["columns"] if x != ""]
        patterns.append(current)
        return patterns

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        total = 0
        for pattern in data:
            horizontal_mirror = self.find_mirror(pattern["rows"])
            if horizontal_mirror is not None:
                total += (horizontal_mirror + 1) * 100
                continue
            vertical_mirror = self.find_mirror(pattern["columns"])
            total += vertical_mirror + 1
        return total

    @staticmethod
    def find_mirror(pattern: list, original_value = None) -> int:
        for i in range(len(pattern) - 1):
            is_mirror = True
            j = 0
            while j <= i and i + j + 1 < len(pattern):
                if pattern[i - j] != pattern[i + j + 1]:
                    is_mirror = False
                j += 1
            if is_mirror:
                if i == original_value:
                    continue
                return i


    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        total = 0
        i = 0
        for main_pattern in data:
            i += 1
            og_horizontal = self.find_mirror(main_pattern["rows"])
            og_vertical = self.find_mirror(main_pattern["columns"])
            found = False
            for pattern in self.modify_pattern(main_pattern):
                if found:
                    break
                horizontal_mirror = self.find_mirror(pattern["rows"], og_horizontal)
                if horizontal_mirror is not None:
                    total += (horizontal_mirror + 1) * 100
                    found = True
                    continue
                vertical_mirror = self.find_mirror(pattern["columns"], og_vertical)
                if vertical_mirror is not None:
                    total += vertical_mirror + 1
                    found = True
                    continue
        return total

    def modify_pattern(self, pattern: dict) -> list:
        length = len(pattern["rows"])
        width = len(pattern["columns"])
        for column in range(width):
            for row in range(length):
                new_pattern = copy.deepcopy(pattern)
                yield self.switch_symbol(new_pattern, row, column)

    @staticmethod
    def switch_symbol(pattern, row, column) -> dict:
        new_char = "#" if pattern["rows"][row][column] == "." else "."
        new_row = pattern["rows"][row][:column] + new_char + pattern["rows"][row][column+1:]
        new_column = pattern["columns"][column][:row] + new_char + pattern["columns"][column][row+1:]
        pattern["rows"][row] = new_row
        pattern["columns"][column] = new_column
        return pattern


if __name__ == "__main__":
    # Load task
    t = Task13()

    # Run task
    t.run_all()
