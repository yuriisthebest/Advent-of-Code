from utils.decorators import timer, debug_shape
from utils.task import Task


class Task3(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 3

    def preprocess(self, data: list) -> dict:
        new_data = {i: {} for i in range(len(data))}
        for i, line in enumerate(data):
            for j, char in enumerate(line):
                if char == ".":
                    continue
                if char.isnumeric():
                    new_data[i][j] = char
                    k = 1
                    while j-k in new_data[i] and new_data[i][j-k].isnumeric():
                        new_data[i][j] = new_data[i][j-k] + char
                        new_data[i][j - k] += char
                        k += 1
                else:
                    new_data[i][j] = char
        return new_data

    @staticmethod
    def check_neighbors(grid: dict, numbers: list, line: int) -> bool:
        """
        Check if a range of numbers has a non-numeric neighbor

        :param line: The line number that the numbers are on
        :param grid: A double dictionary containing all filled spaces with either numbers or non-numerics
        :param numbers: A iterative containing all numbers to check, eq: [1, 2, 3, 4];
        :return: Whether the range of numbers has a non-numeric neighbor in the grid
        """
        found_neighbor = False
        # Check all numbers in iterative
        for num in numbers:
            # Stop early when a neighbor has been found
            if found_neighbor:
                break

            # Check all neighbors
            for neighbor in [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]:
                try:
                    if not grid[line + neighbor[0]][num + neighbor[1]].isnumeric():
                        found_neighbor = True
                        break
                except KeyError:
                    pass
        return found_neighbor

    @staticmethod
    def check_for_gears(grid: dict, numbers: list, line: int) -> list:
        """
        Check if a range of numbers has a gears as neighbors

        :param line: The line number that the numbers are on
        :param grid: A double dictionary containing all filled spaces with either numbers or non-numerics
        :param numbers: A iterative containing all numbers to check, eq: [1, 2, 3, 4];
        :return: Whether the gears that are next to this range of numbers
        """
        gears = []
        # Check all numbers in iterative
        for num in numbers:
            # Check all neighbors
            for neighbor in [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]:
                try:
                    if grid[line + neighbor[0]][num + neighbor[1]] == "*":
                        gears.append((line + neighbor[0], num + neighbor[1]))
                except KeyError:
                    pass
        return gears

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: dict) -> int:
        result = 0
        for i, line in data.items():
            for number in set(line.values()):
                if not number.isnumeric():
                    continue
                # Determine which 'spaces' the numbers in this line occupy
                all_ranges = []
                number_range = []
                for j, value in line.items():
                    if value == number:
                        # There might be duplicate numbers in a line, which causes the number_range to be non-continuous
                        # In that case, save the current number_range and start a new one
                        if len(number_range) > 0 and number_range[-1] != j-1:
                            all_ranges.append(number_range)
                            number_range = []
                        number_range.append(j)
                all_ranges.append(number_range)
                # Check for each number_range (which represents the position of a number) if it has a neighbor
                for number_range in all_ranges:
                    if self.check_neighbors(data, number_range, i):
                        result += int(number)
        return result

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: dict) -> int:
        result = 0
        all_gears = {}
        for i, line in data.items():
            for number in set(line.values()):
                if not number.isnumeric():
                    continue
                # Determine which 'spaces' the numbers in this line occupy
                all_ranges = []
                number_range = []
                for j, value in line.items():
                    if value == number:
                        # There might be duplicate numbers in a line, which causes the number_range to be non-continuous
                        # In that case, save the current number_range and start a new one
                        if len(number_range) > 0 and number_range[-1] != j - 1:
                            all_ranges.append(number_range)
                            number_range = []
                        number_range.append(j)
                all_ranges.append(number_range)
                # Check for each number_range (which represents the position of a number) which gears it is next to
                for number_range in all_ranges:
                    gears = self.check_for_gears(data, number_range, i)
                    for gear in set(gears):
                        # Save which numbers are next to which gears
                        if gear not in all_gears:
                            all_gears[gear] = []
                        all_gears[gear].append(int(number))
        # Calculate the gear ratio
        for parts in all_gears.values():
            if len(parts) == 2:
                result += parts[0] * parts[1]
        return result


if __name__ == "__main__":
    # Load task
    t = Task3()

    # Run task
    t.run_all()
