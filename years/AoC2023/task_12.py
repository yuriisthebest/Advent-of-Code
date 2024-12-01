from utils.decorators import timer, debug
from utils.task import Task

import re


class Task12(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 12

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        total = 0
        print(self.recursion("?.?###", [1, 3]))
        for line in data:
            row = line[0]
            numbers = [int(num) for num in line[1].split(",")]
            arrangements = self.recursion(row, numbers)
            print(f"Line: {row}, possibilities: {arrangements}")
            total += arrangements
        return total
    # 5173 too low
    # 6985 too low

    def recursion(self, row: str, numbers: list) -> int:
        if len(row) == 0:
            if len(numbers) == 0:
                return 1
            return 0
        if row[0] == ".":
            return self.recursion(row[1:], numbers)
        if row[0] == "?":
            return self.recursion(row[1:], numbers) + self.recursion("#" + row[1:], numbers)
        if row[0] == "#":
            if len(numbers) == 0:
                return 0
            if len(row) <= numbers[0]:
                return 0
            if any(row[i] == "." for i in range(numbers[0])):
                return 0
            if row[numbers[0]] == "#":
                return 0
            return self.recursion(row[numbers[0] + 1:], numbers[1:])

    def possible_arrangements(self, row: str, numbers: list) -> int:
        """
        Recursively try to use dots or hashtags to see how many valid arrangements there are

        :param row:
        :param numbers:
        :return:
        """
        if row.count("?") == 0:
            if self.can_be_valid_arrangement(row, numbers, True):
                # print(f"Found: {row}; {numbers}")
                return 1
            return 0
        for i, char in enumerate(row):
            total_possible = 0
            if char == "?":
                # Check if the arrangement could be possible with a .
                dot = row[:i] + "." + row[i+1:]
                if self.can_be_valid_arrangement(dot, numbers):
                    # If the arrangement can be valid, check how many other
                    total_possible += self.possible_arrangements(dot, numbers)
                # Check if the arrangement could be possible with a #
                broken = row[:i] + "#" + row[i+1:]
                if self.can_be_valid_arrangement(broken, numbers):
                    total_possible += self.possible_arrangements(broken, numbers)
                return total_possible

    def can_be_valid_arrangement(self, row: str, numbers: list, recurse: bool = False) -> bool:
        # Check if there are sequences of ? and # possible that
        for num in numbers:
            pattern = "[#?]{NUM}".replace("NUM", str(num))
            match = re.search(pattern, row)
            # print(f"Check: {row}, {numbers}, {num}, {pattern}, {match}, {recurse}")
            # The no possible sequence of the required number can be found, this row cannot be valid
            if match is None:
                return False
            # If the sequence must continue, then the number is incorrect and the row cannot be valid
            for j in range(num):
                if row[match.start() + j] == "?":
                    continue
                if len(row) > match.end() + j and row[match.end() + j] == "#":
                    return False
                else:
                    break
            # If the current number skips a sequence, then there should have been another number in front of this one
            lead = row[:match.end() + 1]
            # if recurse:
            #     print(f"Check: {row}, {numbers}, {num}, {pattern}, {match}, {recurse}, {lead}")
            if num > 1 and recurse:
                for i in range(num-1):
                    if self.can_be_valid_arrangement(lead, [i+1, num], False):
                        # print("Failed")
                        return False
            # This number is correct, remove the part that is used by this number to check for the next number
            row = row[match.end() + 1:]
        else:
            # If there are left-over # in the row, then the numbers are invalid
            if row.count("#") > 0:
                return False
            return True

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        return len(data)


if __name__ == "__main__":
    # Load task
    t = Task12()

    # Run task
    t.run_all()
