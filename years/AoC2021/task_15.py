from utils.decorators import timer, debug_shape
from utils.task import Task
import bisect
import numpy as np
from copy import deepcopy


class Node:
    """
    Object representing a location in the grid of the cave
     This location has a certain risk factor (value) of chitons
     The node also has various of attributes used by Dijkstra's algorithm
    """
    def __init__(self, value: int, x: int, y: int):
        self.value = value
        self.x = x
        self.y = y
        self.locked = False
        self.shortest_distance = 999999999999999
        self.prev_node = None

    def __repr__(self):
        return f"({self.x}, {self.y}: {self.value} ({self.shortest_distance}))"

    def __gt__(self, other):
        return self.shortest_distance > other.shortest_distance

    def neighbors(self, data) -> list:
        """
        Return orthogonal neighbors of this node

        :param data: The grid with all nodes
        :return: List of neighbors of this node
        """
        neighbors = []
        if self.y > 0 and data[self.y - 1][self.x].locked is False:
            neighbors.append(data[self.y - 1][self.x])
        if self.y < len(data[0])-1 and data[self.y + 1][self.x].locked is False:
            neighbors.append(data[self.y + 1][self.x])
        if self.x > 0 and data[self.y][self.x - 1].locked is False:
            neighbors.append(data[self.y][self.x - 1])
        if self.x < len(data)-1 and data[self.y][self.x + 1].locked is False:
            neighbors.append(data[self.y][self.x + 1])
        return neighbors

    def assign_shortest_distance(self, neighbor) -> None:
        if self.shortest_distance > neighbor.shortest_distance + self.value:
            self.shortest_distance = neighbor.shortest_distance + self.value
            self.prev_node = neighbor

    def displace(self, i: int, j: int, len_x: int, len_y: int):
        self.value = self.value + i + j if (self.value + i + j) < 10 else self.value + i + j - 9
        self.x += i * len_x
        self.y += j * len_y
        return self

    def print_path(self) -> str:
        if self.prev_node:
            return f"{self.prev_node.print_path()}, ({self.x}, {self.y})"
        return f"({self.x}, {self.y})"


class Task15(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 15

    def preprocess(self, data: list) -> list:
        """
        Create a grid of numbers

        :param data: List of number strings
        :return: Grid of numbers
        """
        return [[Node(int(value), i, j) for i, value in enumerate(row)] for j, row in enumerate(data)]

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        """
        Dijkstra implementation

        :param data: Grid of nodes representing the cave and chitons risk factor
        :return: Path from top-left to bottom-right with the least risk
        """
        # # Print data
        # for row in data:
        #     print("".join([str(node.value) for node in row]))
        next_nodes = []
        node: Node = data[0][0]
        node.shortest_distance = 0
        while node != data[-1][-1]:
            node.locked = True
            for neighbor in node.neighbors(data):
                neighbor.assign_shortest_distance(node)
                if neighbor not in next_nodes:
                    bisect.insort(next_nodes, neighbor)
            node = next_nodes.pop(0)
        return data[-1][-1].shortest_distance

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Modify the cave grid (data) by multiplying it 25 times
        Find the shortest path on this new grid

        :param data: Grid of nodes representing the cave and chitons risk factor
        :return: Path from top-left to bottom-right with the least risk
        """
        maps = []
        for j in range(5):
            map_row = []
            for i in range(5):
                # Create a new cave map with tweaked values
                original = deepcopy(data)
                cave = [[node.displace(i, j, len(row), len(original)) for node in row] for row in original]
                map_row.append(cave)
            # Concatenate rows together
            maps.append(np.concatenate(map_row, axis=1).tolist())
        data = [row for map_row in maps for row in map_row]
        return self.part_1(data)


if __name__ == "__main__":
    # Load task
    t = Task15()

    # Run task
    t.run_all()
