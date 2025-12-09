from typing import Any

import tqdm

from utils.decorators import timer, debug
from utils.task import Task
from utils.data_structures.tags import Tags
from utils.data_structures.queue import PriorityQueue


class Task9(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 9

    def preprocess(self, data: list) -> list:
        return [tuple([int(num) for num in line.split(',')]) for line in data]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        # Check possible rectangles
        largest_area = 0
        for i, coord in enumerate(data):
            for coord2 in data[i:]:
                if coord == coord2:
                    continue
                area = abs(coord[0] - coord2[0] + 1) * abs(coord[1] - coord2[1] + 1)
                largest_area = area if area > largest_area else largest_area
        return largest_area

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        # Set up the border of the red/green region
        border = set()
        for i, coord in enumerate(data):
            next_coord = data[i+1] if i < len(data) - 1 else data[0]
            variable_dim = None
            for dim in range(len(coord)):
                if coord[dim] != next_coord[dim]:
                    variable_dim = dim
            for step in range(min([coord[variable_dim], next_coord[variable_dim]]),
                              max([coord[variable_dim], next_coord[variable_dim]]) + 1):
                new_coord = list(coord)
                new_coord[variable_dim] = step
                new_coord = tuple(new_coord)
                border.add(new_coord)
        print(f"Border length: {len(border)}")
        # print(border)

        outside_border = set()
        inside_border = set()
        for i, coord in enumerate(data):
            next_coord = data[i + 1] if i < len(data) - 1 else data[0]
            direction = (
                0 if coord[0] == next_coord[0] else 1 if coord[0] < next_coord[0] else -1,
                0 if coord[1] == next_coord[1] else 1 if coord[1] < next_coord[1] else -1
            )
            left = (direction[1], -direction[0])
            right = (-direction[1], direction[0])
            variable_dim = None
            for dim in range(len(coord)):
                if coord[dim] != next_coord[dim]:
                    variable_dim = dim
            for step in range(min([coord[variable_dim], next_coord[variable_dim]]),
                              max([coord[variable_dim], next_coord[variable_dim]]) + 1):
                new_coord = list(coord)
                new_coord[variable_dim] = step
                new_left_coord = (new_coord[0] + left[0], new_coord[1] + left[1])
                if new_left_coord not in border:
                    outside_border.add(new_left_coord)
                new_right_coord = (new_coord[0] + right[0], new_coord[1] + right[1])
                inside_border.add(new_right_coord)
        outside_border = outside_border - inside_border
        print(f"Outborder length: {len(outside_border)}")
        # print(outside_border)

        # Find a sort all possible rectangles
        rectangles = []
        for i, coord in enumerate(data):
            for coord2 in data[i:]:
                if coord == coord2:
                    continue
                rectangles.append((abs(coord[0] - coord2[0] + 1) * abs(coord[1] - coord2[1] + 1), coord, coord2))
        rectangles.sort(key=lambda x: x[0], reverse=True)

        # Check possible rectangles
        for area, coord1, coord2 in tqdm.tqdm(rectangles):
            if self.check_rectangle(coord1, coord2, outside_border):
                return area
        # 1474444748 TOO LOW, took 2800 sec

    # TEST_MODE = True

        # largest_area = 0
        # for i, coord in tqdm.tqdm(enumerate(data)):
        #     for coord2 in data[i:]:
        #         if coord == coord2:
        #             continue
        #         # Check validity if rectangle is completely within red/green area
        #         if not self.check_rectangle(coord, coord2, outside_border):
        #             continue
        #         area =
        #         largest_area = area if area > largest_area else largest_area
        # return largest_area

    def check_rectangle(self, coord1: tuple, coord2: tuple, outside_border: set):
        corners = [
            (coord1[0], coord1[1]),
            (coord1[0], coord2[1]),
            (coord2[0], coord1[1]),
            (coord2[0], coord2[1]),
        ]
        edges = self.edges(corners)
        # print("Rectangle:", coord1, coord2, edges)
        for edge_point in edges:
            if edge_point in outside_border:
                # print(f"OUTSIDE: area = {abs(coord1[0] - coord2[0] + 1) * abs(coord1[1] - coord2[1] + 1)}")
                return False
        # No conflict found, so it's good
        # print(f"IN: area = {abs(coord1[0] - coord2[0] + 1) * abs(coord1[1] - coord2[1] + 1)}")
        return True

    def edges(self, corners: list):
        edges = set()
        for i, coord in enumerate(corners):
            next_coord = corners[i + 1] if i < len(corners) - 1 else corners[0]
            if coord == next_coord:
                continue
            variable_dim = None
            for dim in range(len(coord)):
                if coord[dim] != next_coord[dim]:
                    variable_dim = dim
            for step in range(min([coord[variable_dim], next_coord[variable_dim]]),
                              max([coord[variable_dim], next_coord[variable_dim]]) + 1):
                new_coord = list(coord)
                new_coord[variable_dim] = step
                new_coord = tuple(new_coord)
                edges.add(new_coord)
        return edges


if __name__ == "__main__":
    # Load task
    t = Task9()

    # Run task
    t.run_all()
