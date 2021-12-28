from utils.decorators import timer, debug
from utils.task import Task
import numpy as np


class Range:
    def __init__(self, area: list):
        self.area = area
        self.check_widths()

    def __repr__(self):
        return f" x={self.area[0][0]}..{self.area[0][1]}," \
               f" y={self.area[1][0]}..{self.area[1][1]}," \
               f" z={self.area[2][0]}..{self.area[2][1]}"

    def check_widths(self):
        if self.area[0][0] > self.area[0][1]:
            raise ValueError(f"Range with negative x-width: {self}")
        if self.area[1][0] > self.area[1][1]:
            raise ValueError(f"Range with negative y-width: {self}")
        if self.area[2][0] > self.area[2][1]:
            raise ValueError(f"Range with negative z-width: {self}")

    def overlap(self, other: 'Range') -> bool:
        """
        Check if two ranges overlap

        :param other: The other range to overlap
        :return: True if the two ranges overlap, False otherwise
        """
        # All three ranges must overlap, otherwise the two areas do not overlap
        for i in range(3):
            if len(range(max(self.area[i][0], other.area[i][0]), min(self.area[i][-1], other.area[i][-1]) + 1)) == 0:
                return False
        return True

    def intersection(self, other: 'Range'):
        """
        Determine the area of the overlap

        :param other: Another area that overlaps
        :return: Intersecting area [[min x, max x], [min y, max y], [min z, max z]]
        """
        return [
            [max(self.area[0][0], other.area[0][0]), min(self.area[0][1], other.area[0][1])],
            [max(self.area[1][0], other.area[1][0]), min(self.area[1][1], other.area[1][1])],
            [max(self.area[2][0], other.area[2][0]), min(self.area[2][1], other.area[2][1])]
        ]

    def lit_amount(self):
        return ((self.area[0][1] - self.area[0][0] + 1)
                * (self.area[1][1] - self.area[1][0] + 1)
                * (self.area[2][1] - self.area[2][0] + 1))


class Task22(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 22

    def preprocess(self, data: list) -> list:
        """
        Convert string reboot steps into lists with integers

        :param data: List of reboot steps
        :return: List of reboot steps
        """
        output = []
        for step in data:
            activation = 1 if step[0] == "on" else 0
            coords = step[1].split(',')
            ranges = []
            for coord in coords:
                axis, section = coord.split('=')
                section = [int(num) for num in section.split('..')]
                ranges.append(section)
            output.append([activation, ranges])
        return output

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        """
        Perform reboot initialization

        :param data: List of reboot steps
        :return: Amount of cubes that are on in the reboot initialization procedure region
        """
        grid = np.zeros((101, 101, 101))
        for step in data:
            grid = self.perform_step(grid, [50, 50, 50], step)
        return int(sum(sum(sum(grid))))

    @staticmethod
    def perform_step(grid: np.ndarray, offset: list, step: list) -> np.ndarray:
        """
        Perform one step of the reboot initialization procedure

        :param grid: The grid
        :param offset: Offset of coordinates, the grid works from 0 to N, but it might represent negative areas
        :param step: The step to perform
        :return: Updated grid
        """
        activation = step[0]
        area = [[num + off for num, max_num, off in zip(section, grid.shape, offset)] for section in step[1]]
        grid[area[0][0]:area[0][1] + 1, area[1][0]:area[1][1] + 1, area[2][0]:area[2][1] + 1] = activation
        return grid

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Perform complete reboot

        :param data: List of reboot steps
        :return: Amount of cubes that are on after the reboot
        """
        ons = []
        negs = []

        for i, step in enumerate(data):
            # Create a new range for this step
            new_area = Range(step[1])
            # Check positives for overlap, add negative intersections
            negs_to_add = []
            for area in ons:
                if new_area.overlap(area):
                    # print(f"OVERLAP: {area}, {new_area}")
                    intersection = new_area.intersection(area)
                    intersection = Range(intersection)
                    negs_to_add.append(intersection)
            # Check negatives for overlap, add positive intersections
            for area in negs:
                if new_area.overlap(area):
                    intersection = new_area.intersection(area)
                    intersection = Range(intersection)
                    ons.append(intersection)
            for r in negs_to_add:
                negs.append(r)
            # Add new area to the correct list
            if step[0]:
                ons.append(new_area)

        lit_count = sum([area.lit_amount() for area in ons])
        negative_lit_count = sum([area.lit_amount() for area in negs])
        return lit_count - negative_lit_count


if __name__ == "__main__":
    # Load task
    t = Task22()

    # Run task
    t.run_all()
