from utils.decorators import timer, debug_shape
from utils.task import Task
import numpy as np


class Task25(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 25

    def preprocess(self, data: list) -> np.ndarray:
        """
        Create a numpy array with 0 (empty space), 1 (eastward sea cucumber) and 2 (southward sea cucumber)

        :param data: List of rows of the seabed with sea cucumbers on them
        :return: 2D array contains 0s, 1s and 2s
        """
        grid = np.zeros((len(data), len(data[0])), dtype=np.int8)
        for y, row in enumerate(data):
            for x, char in enumerate(row):
                if char != ".":
                    grid[y, x] = 1 if char == ">" else 2
        return grid

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: np.ndarray) -> int:
        """
        Determine the amount of steps it takes before the sea cucumbers stop moving

        :param data: 2D grid representing the positions of the sea cucumbers
        :return: Amount of steps until sea cucumbers stop moving
        """
        i = 0
        has_changed = True
        grid = data
        # Keep simulating steps until the sea cucumbers stop moving
        while has_changed:
            # The sea cucumbers first move to the east, then to the south
            grid, moved_east = self.move_east(grid)
            grid, moved_south = self.move_south(grid)
            has_changed = True if moved_east or moved_south else False
            i += 1
        return i

    @staticmethod
    def move_east(grid: np.ndarray, assigned: int = 1):
        has_moved = False
        for y, row in enumerate(grid):
            skip_next = False
            first_filled = True if row[0] != 0 else False
            for x, char in enumerate(row):
                if skip_next:
                    skip_next = False
                    continue
                # A east facing sea cucumber will only move if the place to its right is free
                if char == assigned and grid[y, (x + 1) % len(row)] == 0:
                    # The final sea cucumber in the row must first look if the first spot used to be filled
                    if x == len(row) - 1 and first_filled:
                        continue
                    grid[y, x] = 0
                    grid[y, (x + 1) % len(row)] = assigned
                    skip_next = True
                    has_moved = True
        return grid, has_moved

    def move_south(self, grid: np.ndarray):
        """
        Move south by transposing the grid, such that moving east actually moves south

        :param grid:
        :return:
        """
        grid = grid.transpose()
        grid, has_moved = self.move_east(grid=grid, assigned=2)
        grid = grid.transpose()
        return grid, has_moved

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: np.ndarray) -> str:
        """
        Find the sleigh keys, boost the signal, save christmas
        """
        return "BOOSTING SIGNAL... WE DID IT... WE SAVED CHRISTMAS!!!"


if __name__ == "__main__":
    # Load task
    t = Task25()

    # Run task
    t.run_all()
