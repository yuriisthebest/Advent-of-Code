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
        lines = [tuple([int(num) for num in line.split(',')]) for line in data]
        all_nums = []
        for line in lines:
            all_nums.extend(line)
        all_nums.sort()
        all_nums = {val: i+1 for i, val in enumerate(all_nums)}
        return ([tuple([all_nums[line[0]], all_nums[line[1]]]) for line in lines], all_nums)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        data = data[0]
        translation = data[1]
        # Check possible rectangles
        largest_area = 0
        best_coords = None
        for i, coord in enumerate(data):
            for coord2 in data[i:]:
                if coord == coord2:
                    continue
                area = abs(coord[0] - coord2[0] + 1) * abs(coord[1] - coord2[1] + 1)
                if area > largest_area:
                    largest_area = area
                    best_coords = (coord, coord2)
        x1 = list(translation.keys())[list(translation.values()).index(best_coords[0][0])]
        x2 = list(translation.keys())[list(translation.values()).index(best_coords[1][0])]
        y1 = list(translation.keys())[list(translation.values()).index(best_coords[0][1])]
        y2 = list(translation.keys())[list(translation.values()).index(best_coords[1][1])]
        largest_area = abs(x1 - x2) * abs(y1 - y2)
        return largest_area

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        # Set up the border of the red/green region
        data = data[0]
        translation = data[1]
        border = []
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
                border.append(new_coord)
        # Setup internal nodes
        middle = (50000, 50000) if not self.IS_TEST else (10, 5)
        _, internals = self.has_path(middle, (0, 0), border, True)
        print(len(internals))
        # Check possible rectangles
        largest_area = 0
        best_coords = None
        for i, coord in tqdm.tqdm(enumerate(data)):
            for coord2 in data[i:]:
                if coord == coord2:
                    continue
                # Check validity if rectangle is completely within red/green area
                if not self.check_rectangle(coord, coord2, border, internals):
                    continue
                area = abs(coord[0] - coord2[0] + 1) * abs(coord[1] - coord2[1] + 1)
                if area > largest_area:
                    largest_area = area
                    best_coords = (coord, coord2)
        x1 = list(translation.keys())[list(translation.values()).index(best_coords[0][0])]
        x2 = list(translation.keys())[list(translation.values()).index(best_coords[1][0])]
        y1 = list(translation.keys())[list(translation.values()).index(best_coords[0][1])]
        y2 = list(translation.keys())[list(translation.values()).index(best_coords[1][1])]
        largest_area = abs(x1-x2) * abs(y1-y2)
        return largest_area

    def check_rectangle(self, coord1: tuple, coord2: tuple, border: list, internals: set):
        corners = [
            (coord1[0], coord1[1]),
            (coord1[0], coord2[1]),
            (coord2[0], coord1[1]),
            (coord2[0], coord2[1]),
        ]
        edges = self.edges(corners)
        # print(f"Checking rectangle with edges: {edges} AND THE BORDER: {border}")
        for edge_point in edges:
            # print(f"Checking {edge_point}")
            # If the edge point is on the border, it's within the red/green area
            if edge_point in border or edge_point in internals:
                # print(f"Point {edge_point} on border")
                continue
            # Check if the point is within the red/green area of outside
            # Check by pathfinding to 0,0 without crossing the border
            # if self.has_path(edge_point, (0, 0), border):
                # print(f"Point {edge_point} has a path to 0,0")
            else:
                return False
        # No conflict found, so it's good
        return True

    def has_path(self, start: tuple, end_point: tuple, border: list, get_seen: bool = False):
        seen = set()
        todo = PriorityQueue("distance")
        todo.add(Node(start))
        while len(todo) > 0:
            node = todo.take_first().coord
            if node == end_point:
                return True if not get_seen else True, seen
            seen.add(node)
            n1 = (node[0] - 1, node[1])
            n2 = (node[0], node[1] - 1)
            n3 = (node[0] + 1, node[1])
            n4 = (node[0], node[1] + 1)
            if n1 not in border and n1 not in seen:
                seen.add(n1)
                todo.add(Node(n1))
            if n2 not in border and n2 not in seen:
                seen.add(n2)
                todo.add(Node(n2))
            if n3 not in border and n3 not in seen:
                seen.add(n3)
                todo.add(Node(n3))
            if n4 not in border and n4 not in seen:
                seen.add(n4)
                todo.add(Node(n4))
        return False if not get_seen else False, seen

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

    # TEST_MODE = True


class Node:
    def __init__(self, coord: tuple):
        super().__init__()
        self.coord = coord

    def __lt__(self, other):
        return self.get("") < other.get("")

    def __repr__(self):
        return str(self.coord)

    def get(self, tag_name: str):
        return abs(self.coord[0]) + abs(self.coord[1])


if __name__ == "__main__":
    # Load task
    t = Task9()

    # Run task
    t.run_all()
