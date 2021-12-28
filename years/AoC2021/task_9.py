from utils.decorators import timer, debug
from utils.task import Task


def is_low_point(data: list, i: int, j: int) -> bool:
    """
     Return whether the neighboring numbers are all higher or not
    """
    p = data[i][j]
    if j > 0 and p >= data[i][j - 1]:
        return False
    if j < len(data[0]) - 1 and p >= data[i][j + 1]:
        return False
    if i > 0 and p >= data[i - 1][j]:
        return False
    if i < len(data) - 1 and p >= data[i + 1][j]:
        return False
    return True


def find_basin(data, i, j, basin):
    """
    Recursive function to find all points belonging to a basin, starting with any number in the basin
    """
    basin.append((i, j))
    if j > 0 and (i, j - 1) not in basin and data[i][j - 1] != 9:
        basin = find_basin(data, i, j - 1, basin)
    if j < len(data[0]) - 1 and (i, j + 1) not in basin and data[i][j + 1] != 9:
        basin = find_basin(data, i, j + 1, basin)
    if i > 0 and (i - 1, j) not in basin and data[i - 1][j] != 9:
        basin = find_basin(data, i - 1, j, basin)
    if i < len(data) - 1 and (i + 1, j) not in basin and data[i + 1][j] != 9:
        basin = find_basin(data, i + 1, j, basin)
    return basin


class Task9(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 9

    def preprocess(self, data: list) -> list:
        grid = []
        for row in data:
            new_row = []
            for element in row:
                new_row.append(int(element))
            grid.append(new_row)
        return grid

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        """
        Find and return the numbers in a closed grid whose neighbors are all higher (return smallest numbers)

        :param data: Grid with numbers
        :return: The sum of the low points of the grid
        """
        low_points = []
        for i in range(len(data)):
            for j in range(len(data[0])):
                if is_low_point(data, i, j):
                    low_points.append(data[i][j] + 1)
        return sum(low_points)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Find the three largest basins (areas surrounded by 9s) in the grid

        :param data: Grid of numbers
        :return: Product of the three largest basins
        """
        # Find low points (each low point creates one basin)
        low_points = []
        for i in range(len(data)):
            for j in range(len(data[0])):
                if is_low_point(data, i, j):
                    low_points.append((i, j))
        # Find the basin (sizes) from the low points
        basin_sizes = []
        for basin in low_points:
            basin_sizes.append(len(find_basin(data, basin[0], basin[1], [])))
        # Take the three largest basins and calculate their product
        basin_sizes.sort()
        basin_sizes = basin_sizes[-3:]
        answer = 1
        for size in basin_sizes:
            answer *= size
        return answer


if __name__ == "__main__":
    # Load task
    t = Task9()

    # Run task
    t.run_all()
