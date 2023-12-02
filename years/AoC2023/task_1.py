from utils.decorators import timer, debug
from utils.task import Task

import re


class Task1(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 1

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        max_sum = 0
        for i, string in enumerate(data):
            first = None
            last = None
            # Check every character in string
            for char in string:
                if char.isnumeric():
                    if first is None:
                        first = int(char)
                    last = int(char)
            # If line does not contain digits, set values to 0
            if first is None or last is None:
                first = 0
                last = 0
            # Calculate score of current line
            max_sum += (10 * first) + last
        return max_sum

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        max_sum = 0
        written_letters = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        for i, string in enumerate(data):
            first = None
            last = None
            # Split the string into chunks of numbers and non-numbers
            match = re.split(r"(\d+)", string)
            for group in match:
                lowest_index = 999
                max_index = -1
                # Check non-number groups
                if not group.isnumeric():
                    for num in written_letters:
                        # Check if written letter is in group
                        index = group.find(num)
                        if index != -1:
                            if index < lowest_index:
                                lowest_index = index
                            if index > max_index:
                                max_index = index

                            # Check if the same written letter is more often in group
                            updated = True
                            new_index = index
                            while updated is True:
                                new_index = group.find(num, new_index+1, len(group)+1)
                                if new_index != -1 and new_index > max_index:
                                    max_index = new_index
                                else:
                                    updated = False
                    # Identify the lowest written number
                    if first is None and lowest_index != 999:
                        # Iteratively expand the substring until a written number is found
                        i = 0
                        while first is None:
                            try:
                                first = written_letters.index(group[lowest_index:lowest_index+i]) + 1
                            except ValueError:
                                pass
                            i += 1
                    # Identify the max written number
                    if max_index != -1:
                        # Iteratively expand the substring until a written number is found
                        for j in range(10):
                            try:
                                result = written_letters.index(group[max_index:max_index + j]) + 1
                                if result != -1:
                                    last = result
                                    break
                            except ValueError:
                                pass
                # Check numbers
                if group.isnumeric():
                    for num in group:
                        if first is None:
                            first = int(num)
                        last = int(num)
            # Calculate score of current line
            max_sum += (10 * first) + last
        return max_sum


if __name__ == "__main__":
    # Load task
    t = Task1()

    # Run task
    t.run_all()
