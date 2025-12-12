import numpy as np
from abc import abstractmethod
from typing import List
from itertools import product

from utils import load
from utils.data_structures.queue import PriorityQueue
from utils.data_structures.tags import Tags


class Cell(Tags):
    """
    A Cell is a single element within a grid that has a position in the grid, a possible value and possible tags
    """
    def __init__(self, position: tuple, value: any = None) -> None:
        """
        Create a cell with a position and optional value

        :param position: A tuple representing the coordinates of the cell
        :param value: A specific value assigned to the cell
        """
        super().__init__()
        self.__position = position
        # Default tag based on input value
        self.update_tag({"value": value, "locked": False})

    def __repr__(self) -> str:
        """
        A cell is represented by its value

        :return: the value of the cell
        """
        return str(self.get("value")) if self.get("value") is not None else " "

    def __lt__(self, other):
        # specifify what tag to compare against; default comparison is 'value'
        sort_tag = self.get("sort_tag") if self.has_tag("sort_tag") else "value"
        return self.get(sort_tag) < other.get(sort_tag)

    def __hash__(self):
        return hash(tuple([(key, value) for key, value in self.get_all_tags().items()]))

    def get_pos(self) -> tuple:
        """
        Retrieve the coordinates of the cell
        """
        return self.__position

    def manhattan_distance(self, other) -> int:
        """
        Calculates the manhattan distance to another Cell

        :param other: Another cell in the grid
        :return: The manhattan disctance between this Cell and the given one
        """
        return sum([abs(i-j) for i, j in zip(self.get_pos(), other.get_pos())])


class Grid:
    """
    Data structure to aid tasks involving grids. Used for naive solutions where the entire grid can be stored in memory.
    """
    def __init__(self, data: list, edge_included: bool = False, wrap_around: bool = False) -> None:
        """
        Create a grid from the given data

        :param data: list containing horizontal rows of the grid, from top to bottom.
        :param edge_included: does the input data include an edge character?
        :param wrap_around: does the grid wrap around from right or left and bottom to top?
        """
        self.wrap_around = wrap_around
        # Build a grid with cells from the relevant input data
        if edge_included:
            self.grid = [[Cell(position=(i, j), value=char)
                          for j, char in enumerate(line[1:-1])]
                         for i, line in enumerate(data[1:-1])]
        else:
            self.grid = [[Cell(position=(i, j), value=char)
                          for j, char in enumerate(line)]
                         for i, line in enumerate(data)]
        self.max_dims = []
        # Determine the maximum length of each dimension
        dims = self.grid
        while isinstance(dims, list):
            self.max_dims.append(len(dims))
            dims = dims[0]

    def get_cell(self, position: tuple) -> Cell:
        """
        Return the Cell in the given position in the grid.
        TODO: current implementation assumes a position that is within the grid

        :param position: A tuple representing a position in the grid
        :return: Cell
        """
        cell = self.grid
        for dim_position in position:
            cell = cell[dim_position]
        return cell

    def contains_cell(self, position: tuple) -> bool:
        """
        Check if a given position in within the grid

        :param position: A tuple representing a position in the grid
        :return: True if the position is within the grid, otherwise False
        """
        for i, dim_position in enumerate(position):
            if dim_position < 0 or dim_position >= self.max_dims[i]:
                return False
        return True

    def get_each_cells(self):
        for line in self.grid:
            for cell in line:
                yield cell

    def find_values(self, tag: str = "value", values: list = None, stop_on_found: bool = True) -> Cell | List[Cell]:
        """
        Finds cells based on their value for a specific tag

        :param tag: The tag to search the cells for; Default: "value"
        :param values: A list of values to screen for
        :param stop_on_found: if True, only return the first cell with a value matching the search criteria
        :return: Cell(s) matching the search value criteria
        """
        if values is None:
            raise ValueError(f"values must be given in function 'find_values', currently: {values}")
        found = []
        for line in self.grid:
            for cell in line:
                if cell.get(tag) in values:
                    if stop_on_found:
                        return cell
                    found.append(cell)
        return found

    def get_adjacent(self, cell: Cell, ortogonal: bool = True, allow: dict = None, disallow: dict = None) -> List[Cell]:
        """
        Get all the neighbors of a given Cell.
        Filter on ortoganality, allow certain values or disallowed certain values

        :param cell: The current Cell whose neighbors to get
        :param ortogonal: only get ortogonal neighbors are also 'indirect' neighbors
        :param allow: A key-value dictionary indicating a mandatory filter of tags and value-lists
        :param disallow: A key-value dictionary indicating a forbidden filter of tags and value-lists
        :return: List of Cell that are (allowed) neighbors of the given Cell
        """
        try_directions = list(product([-1, 0, 1], repeat=len(cell.get_pos())))
        if ortogonal:
            try_directions = [direction for direction in try_directions if direction.count(0) == len(direction) - 1]
        # Try and filter neighbors
        neighbors = []
        for direction in try_directions:
            new_pos = list(map(sum, zip(direction, cell.get_pos())))
            # Ignore the cell self
            if tuple(new_pos) == cell.get_pos():
                continue
            # Check if neighbor falls within the grid
            within_grid = True
            for i, coordinate in enumerate(new_pos):
                if not self.wrap_around and (coordinate < 0 or coordinate >= self.max_dims[i]):
                    within_grid = False
                    break
                else:
                    new_pos[i] = coordinate % self.max_dims[i]
            if not within_grid:
                continue
            # Get the appropiate cell
            potential_neighbor = self.get_cell(tuple(new_pos))
            # Check if cell is allowed or disallowed
            if allow is not None:
                allowed = True
                for tag in allow.keys():
                    if potential_neighbor.get(tag) not in allow[tag]:
                        allowed = False
                        break
                if not allowed:
                    continue
            if disallow is not None:
                allowed = True
                for tag in disallow.keys():
                    if potential_neighbor.get(tag) in disallow[tag]:
                        allowed = False
                        break
                if not allowed:
                    continue
            # Add valid neighbor to output
            neighbors.append(potential_neighbor)
        return neighbors

    def find_path(self, source: Cell, target: Cell, allow: dict = None, disallow: dict = None) -> int:
        """
        Finds a path from one Cell to another.

        :param source: The starting cell
        :param target: The ending cell
        :param allow: A key-value dictionary indicating a mandatory filter of tags and value-lists
        :param disallow: A key-value dictionary indicating a forbidden filter of tags and value-lists
        :return: The distance of the path, returns -1 if no path can be found
        """
        # Prepare priority queue
        sort_tag = "A*"
        todo = PriorityQueue(tag=sort_tag)
        source.update_tag({"distance": 0, sort_tag: 0, "sort_tag": sort_tag})
        todo.add(source)
        while len(todo) != 0:
            # Take the least travelled non-locked cell
            node = todo.take_first()
            node.update_tag({"locked": True})
            # For each neighbor, see if it's locked, see if going there is an improvement, add it to the queue
            for neighbor in self.get_adjacent(node, allow=allow, disallow=disallow):
                if neighbor.get("locked"):
                    continue
                distance = node.get("distance") + self.__move_cost(neighbor, node) + self.__heuristic(neighbor, target)
                if not neighbor.has_tag(sort_tag) or neighbor.get(sort_tag) < distance:
                    neighbor.update_tag({"previous": node,
                                         "distance": distance - self.__heuristic(neighbor, target),
                                         sort_tag: distance,
                                         "sort_tag": sort_tag})
                    todo.add(neighbor)
                # Stop the search if the target has been found
                if neighbor == target:
                    return neighbor.get("distance")
        return -1

    @abstractmethod
    def __move_cost(self, current_cell: Cell, previous_cell: Cell) -> int:
        return 1

    @abstractmethod
    def __heuristic(self, current_cell: Cell, end_cell: Cell) -> int:
        return current_cell.manhattan_distance(end_cell)

    def __repr__(self) -> str:
        output = ""
        for line in self.grid:
            output += str(line)+"\n"
        return output

    def __len__(self):
        return self.max_dims

    def __array__(self, dtype=None):
        return np.array(self.grid, dtype=dtype)

    def __hash__(self):
        return hash(tuple([tuple([cell for cell in line]) for line in self.grid]))


if __name__ == "__main__":
    # Task 16 of 2024 contained a grid, use it to test the Grid class
    path = "../../data/AoC2024/task16_data.txt"
    task = load.__load_txt(path)
    grid = Grid(task, edge_included=True)
    # Find specific cells
    print(f'Find first #: {grid.find_values("value", ["#"], stop_on_found=True).get_pos()}')
    print(f'Find all #: {len(grid.find_values("value", ["#"], stop_on_found=False))}')
    # Get neighbors
    n = grid.get_adjacent(grid.grid[1][0], ortogonal=True)
    print(f"Ortogonal neighbors: {n}")
    n = grid.get_adjacent(grid.grid[1][0], ortogonal=True, allow={"value": ['#']})
    print(f"Ortogonal neighbors with value '#': {n}")
    # Get path
    s = grid.get_cell((0, 0))
    e = grid.get_cell((2, 4))
    d = grid.find_path(s, e, disallow={"value": "#"})
    # 8 Neighbors
    n = grid.get_adjacent(grid.grid[1][0], ortogonal=False)
    print(f"Non-ortogonal neighbors: {n}, {[cell.get_pos() for cell in n]}; Self position: {grid.grid[1][0].get_pos()}")
    print(f"Find path distance: {d}")
    ns = e
    path = [ns.get_pos()]
    while ns != s:
        ns = ns.get("previous")
        path.append(ns.get_pos())
    print(f"Find path: {path[::-1]}")
    print(e.has_tag("test"))
    print(e.get("test"))
