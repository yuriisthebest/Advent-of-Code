from utils.decorators import timer, debug
from utils.task import Task


class Tile:
    def __init__(self, x: int, y: int):
        self.column = x
        self.row = y
        self.neighbors = []
        self.unavailability = {}

    def __repr__(self):
        return f"(C{self.column}, R{self.row})"

    def manhattan(self, other):
        return abs(self.column - other.column) + abs(self.row - other.row)

    def assign_unavailability(self, time: int, modulo: int):
        if modulo not in self.unavailability:
            self.unavailability[modulo] = set()
        self.unavailability[modulo].add(time)

    def is_available(self, time: int):
        """
        Check if the tile is available at a certain time

        :param time: The time to check
        :return: Whether the current tile is available
        """
        for mod in self.unavailability.keys():
            for value in self.unavailability[mod]:
                # If the current time is equal to an unavailable time, the tile is currently unavailable
                if time % mod == value:
                    return False
        # No blizzards are currently on this tile, so it's available
        return True


class Task24(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 24

    def preprocess(self, data: list) -> tuple:
        tiles = {y - 1: {x - 1: Tile(x - 1, y - 1)
                         for x, tile in enumerate(line) if tile != "#"}
                 for y, line in enumerate(data)}
        # Assign neighbors
        for row in tiles:
            for column in tiles[row]:
                for rel_coord in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    # Add neighbor, if it exists
                    if row + rel_coord[0] in tiles and column + rel_coord[1] in tiles[row + rel_coord[0]]:
                        tiles[row][column].neighbors.append(tiles[row + rel_coord[0]][column + rel_coord[1]])
        for j, line in enumerate(data):
            j -= 1
            for i, tile in enumerate(line):
                i -= 1
                if tile == '#':
                    continue
                # Found a blizzard, proces it
                if tile != ".":
                    if tile == ">":
                        for x in range(len(line) - 2):
                            mod = len(line) - 2
                            tiles[j][(i + x) % mod].assign_unavailability(x, mod)
                    if tile == "<":
                        for x in range(len(line) - 2):
                            mod = len(line) - 2
                            tiles[j][(i - x) % mod].assign_unavailability(x, mod)
                    if tile == "^":
                        for x in range(len(data) - 2):
                            mod = len(data) - 2
                            tiles[(j - x) % mod][i].assign_unavailability(x, mod)
                    if tile == "v":
                        for x in range(len(data) - 2):
                            mod = len(data) - 2
                            tiles[(j + x) % mod][i].assign_unavailability(x, mod)
        # Find source and target
        source = (-1, 0)
        target = (len(data) - 2, list(tiles[len(data) - 2].keys())[0])
        return tiles, source, target

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: tuple) -> int:
        tiles, source, target = data
        target = tiles[target[0]][target[1]]
        todo = [(0, tiles[source[0]][source[1]].manhattan(target), tiles[source[0]][source[1]])]
        # Run A* to find the shortest route
        while len(todo) != 0:
            time, heuristic, tile = todo.pop()
            # Stop if we reached the target
            if tile == target:
                return time + 1
            # Wait
            todo.append((time + 1, heuristic + 1, tile))
            # Go to neighbor
            for neighbor_tile in tile.neighbors:
                if neighbor_tile.is_available(time + 1):
                    todo.append((time + 1, neighbor_tile.manhattan(target) + time + 1, neighbor_tile))
            todo.sort(key=lambda x: x[1], reverse=True)
        return -1

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: tuple) -> int:
        return len(data[0])


if __name__ == "__main__":
    # Load task
    t = Task24()

    # Run task
    t.run_all()
