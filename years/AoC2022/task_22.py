import re
from utils.decorators import timer, debug_shape
from utils.task import Task


class Node:
    def __init__(self, tile: str, row: int, column: int):
        self.tile = tile
        self.row = row
        self.column = column
        self.neighbors = []

    def __repr__(self):
        return f"'{self.tile}'" + f": {[(x.row, x.column) for x in self.neighbors]}"


class Task22(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 22
    # Right, Down, Left, Up
    CHECK_DIRECTION = {
        0: (0, 1),
        1: (1, 0),
        2: (0, -1),
        3: (-1, 0),
    }

    def preprocess(self, data: list) -> tuple:
        grid = {i: self.process_line(line, i) for i, line in enumerate(data[:-2])}
        return grid, data[-1]

    def assign_neighbors_on_map(self, grid):
        width = max([max(grid[i]) for i in range(len(grid))]) + 1
        height = len(grid)
        for row in grid:
            for column in grid[row]:
                tile = grid[row][column]
                # Assign the neighbors for each tile
                for check in self.CHECK_DIRECTION.values():
                    i = 1
                    # Check if the neighbor exists, or move one over to find it
                    while ((tile.row + check[0] * i) % height not in grid
                           or (tile.column + check[1] * i) % width not in grid[(tile.row + check[0] * i) % height]):
                        i += 1
                    tile.neighbors.append(
                        grid[(tile.row + check[0] * i) % height][(tile.column + check[1] * i) % width])

    def assign_neighbors_on_dice(self, grid):
        width = max([max(grid[i]) for i in range(len(grid))]) + 1
        height = len(grid)
        for row in grid:
            for column in grid[row]:
                tile = grid[row][column]
                # Assign the neighbors for each tile
                for direction, check in enumerate(self.CHECK_DIRECTION.values()):
                    # Check if the neighbor exists, or move over the edge
                    if ((tile.row + check[0]) % height in grid
                            and (tile.column + check[1]) % width in grid[(tile.row + check[0]) % height]):
                        tile.neighbors.append(
                            (grid[(tile.row + check[0]) % height][(tile.column + check[1]) % width]), direction)
                    else:
                        # Go over the edge of the dice and determine the new facing direction
                        pass

    @staticmethod
    def process_line(line: list, row: int) -> dict:
        processed_line = {}
        i = 0
        for tile in line:
            if len(tile) <= 1:
                if tile != "":
                    processed_line[i] = Node(tile, row, i)
                i += 1
            else:
                for thing in tile:
                    if thing != "":
                        processed_line[i] = Node(thing, row, i)
                    i += 1
        return processed_line

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: tuple) -> int:
        grid, commands = data
        self.assign_neighbors_on_map(grid)
        # Start moving
        direction = 0
        position = (0, min(grid[0]))
        commands = re.split('(\d+)', commands)[1:-1]
        # Follow the commands of the monkeys
        for command in commands:
            match command:
                case "R":
                    direction += 1
                    direction %= 4
                case "L":
                    direction -= 1
                    direction %= 4
                case _:
                    position = self.move_on_map(grid, position, direction, int(command))
        return (position[0] + 1) * 1000 + (position[1] + 1) * 4 + direction

    @staticmethod
    def move_on_map(grid: dict, position: tuple, direction: int, distance: int) -> tuple:
        new_position = position
        for step in range(distance):
            y, x = new_position
            neighbor = grid[y][x].neighbors[direction]
            # Stop if we meet a wall
            if neighbor.tile == "#":
                return new_position
            new_position = neighbor.row, neighbor.column
        return new_position

    @staticmethod
    def move_on_dice(grid: dict, position: tuple, direction: int, distance: int) -> tuple:
        new_position = position
        new_direction = direction
        # Do X steps
        for step in range(distance):
            y, x = new_position
            neighbor, new_direction = grid[y][x].neighbors[new_direction]
            # Stop if we meet a wall
            if neighbor.tile == "#":
                return new_position, new_direction
            new_position = neighbor.row, neighbor.column
        return new_position, new_direction

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: tuple) -> int:
        grid, commands = data
        self.assign_neighbors_on_dice(grid)
        # Start moving
        direction = 0
        position = (0, min(grid[0]))
        commands = re.split('(\d+)', commands)[1:-1]
        # Follow the commands of the monkeys
        for command in commands:
            match command:
                case "R":
                    direction += 1
                    direction %= 4
                case "L":
                    direction -= 1
                    direction %= 4
                case _:
                    position, direction = self.move_on_dice(grid, position, direction, int(command))
        return (position[0] + 1) * 1000 + (position[1] + 1) * 4 + direction


if __name__ == "__main__":
    # Load task
    t = Task22()

    # Run task
    t.run_all()
