import copy
from functools import cache

from utils.decorators import timer, debug
from utils.task import Task
from utils.data_structures.grid import Grid


class Task12(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 12

    def preprocess(self, data: list) -> tuple:
        presents = []
        regions = []
        for i, line in enumerate(data):
            # Process present
            if line != "" and line[-1] == ":":
                presents.append(tuple(data[i+1:i+4]))
            # Process region
            elif isinstance(line, list):
                regions.append((tuple([int(num) for num in line[0][:-1].split("x")]), [int(num) for num in line[1:]]))
        return presents, regions

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: tuple) -> int:
        fits = 0
        presents, regions = data
        for region in regions:
            if self.check_region(region, tuple(presents)):
                fits += 1
        return fits

    def check_region(self, region: list, shapes: tuple) -> bool:
        size = region[0]
        requirements = tuple(region[1])
        pip_count = [sum([line.count("#") for line in shape]) for shape in shapes]
        total_pips = sum([num_shape * num_pip for num_shape, num_pip in zip(requirements, pip_count)])
        # If the total area of the required shapes is larger than the available area, it's not possible
        if total_pips > size[0] * size[1]:
            return False
        # If there are more 3x3 areas than shapre required, it's automatically good
        easy_shapes = (size[0] // 3) * (size[1] // 3)
        if sum(requirements) <= easy_shapes:
            return True
        # Try to fit the region
        print("Checking fit")
        grid = Grid([["." for _ in range(size[1])] for _ in range(size[0])])
        return self.fit_region(grid, requirements, shapes)

    @cache
    def fit_region(self, grid: Grid, requirements: tuple, shapes: tuple):
        """
        Recursively fill the grid with shapes

        :param grid:
        :param requirements:
        :param shapes:
        :return:
        """
        return False
        if sum(requirements) == 0:
            print(f"Managed to fit everything!\n{grid}")
            return True
        for i, value in enumerate(requirements):
            if value > 0:
                for cell in grid.get_each_cells():
                    shape = shapes[i]
                    for permutations in self.permute_shape(shape):
                        if self.check_shape(grid, permutations, cell.get_pos()):
                            # print(f"Found a spot: {cell.get_pos()}\n{permutations}\n{grid}")
                            new_grid = copy.deepcopy(grid)
                            new_grid = self.place_shape(new_grid, permutations, cell.get_pos())
                            # Place the shape and try a new one
                            new_reqs = tuple([num if x != i else num - 1 for x, num in enumerate(requirements)])
                            result = self.fit_region(new_grid, new_reqs, shapes)
                            if result:
                                return True
                return False
        return False

    def check_shape(self, grid: Grid, shape: tuple, coord: tuple) -> bool:
        """
        Check if a shape fits at a specific coordinate

        :param grid:
        :param shape:
        :param coord:
        :return:
        """
        for i in range(3):
            for j in range(3):
                check_coord = (coord[0] + i, coord[1] + j)
                if not grid.contains_cell((coord[0] + i, coord[1] + j)):
                    return False
                # If the shape wants to be placed where there already is a shape, it can't fit
                if shape[i][j] == "#" and grid.get_cell(check_coord).get("value") == "#":
                    return False
        return True

    def place_shape(self, grid: Grid, shape: tuple, coord: tuple) -> Grid:
        for i in range(3):
            for j in range(3):
                if shape[i][j] == ".":
                    continue
                grid.get_cell((coord[0] + i, coord[1] + j)).update_tag({"value": "#"})
        return grid

    @cache
    def permute_shape(self, shape: tuple) -> set:
        """
        Rotate and flip the shape to create all possible shapes
        :param shape: The shape to rotate and flip
        :return: List of possible shapes
        """
        possible_shapes = set()
        for permutation_matrix in [
            [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)]],  # normal
            [[(2, 0), (2, 1), (2, 2)], [(1, 0), (1, 1), (1, 2)], [(0, 0), (0, 1), (0, 2)]],  # flipped-y normal
            [[(0, 2), (0, 1), (0, 0)], [(1, 2), (1, 1), (1, 0)], [(2, 2), (2, 1), (2, 0)]],  # flipped-x normal
            [[(2, 0), (1, 0), (0, 0)], [(2, 1), (1, 1), (0, 1)], [(2, 2), (1, 2), (0, 2)]],  # rotated once
            [[(2, 2), (1, 2), (0, 2)], [(2, 1), (1, 1), (0, 1)], [(2, 0), (1, 0), (0, 0)]],  # flipped-y rotated once
            [[(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)]],  # flipped-x rotated once
            [[(2, 2), (2, 1), (2, 0)], [(1, 2), (1, 1), (1, 0)], [(0, 2), (0, 1), (0, 0)]],  # rotated twice
            # [[(0, 2), (0, 1), (0, 0)], [(1, 2), (1, 1), (1, 0)], [(2, 2), (2, 1), (2, 0)]],  # flipped-y rotated twice
            # [[(2, 0), (2, 1), (2, 2)], [(1, 0), (1, 1), (1, 2)], [(0, 0), (0, 1), (0, 2)]],  # flipped-x rotated twice
            [[(0, 2), (1, 2), (2, 2)], [(0, 1), (1, 1), (2, 1)], [(0, 0), (1, 0), (2, 0)]],  # rotated thrice
        ]:
            new_shape = tuple([tuple([shape[coord[0]][coord[1]] for coord in line]) for line in permutation_matrix])
            possible_shapes.add(new_shape)
        return possible_shapes

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: tuple) -> int:
        return -1


if __name__ == "__main__":
    # Load task
    t = Task12()

    # Run task
    t.run_all()
