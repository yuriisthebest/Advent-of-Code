import itertools

from utils.decorators import timer, debug_shape
from utils.task import Task


def manhattan_distance(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


class Task12(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 12

    def preprocess(self, data: list) -> list:
        return [[ord(char) - 96 if char != "E" else 99 for char in row] for row in data]

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        # Coordinates: (ROW, COLUMN)
        source = [(i, row.index(-13)) for i, row in enumerate(data) if -13 in row][0]
        target = [(i, row.index(99)) for i, row in enumerate(data) if 99 in row][0]
        data[source[0]][source[1]] = 1
        data[target[0]][target[1]] = 26
        return self.find_sortest_path(data, source, target)

    @staticmethod
    def find_neighbors(data: list, coord: tuple) -> list:
        # Check for validity
        height = data[coord[0]][coord[1]]
        neighbors = []
        if coord[0] + 1 < len(data) and height + 1 >= data[coord[0] + 1][coord[1]]:
            neighbors.append((coord[0] + 1, coord[1]))
        if coord[0] - 1 >= 0 and height + 1 >= data[coord[0] - 1][coord[1]]:
            neighbors.append((coord[0] - 1, coord[1]))
        if coord[1] + 1 < len(data[coord[0]]) and height + 1 >= data[coord[0]][coord[1] + 1]:
            neighbors.append((coord[0], coord[1] + 1))
        if coord[1] - 1 >= 0 and height + 1 >= data[coord[0]][coord[1] - 1]:
            neighbors.append((coord[0], coord[1] - 1))
        # print(f"New n: {neighbors} of {coord}")
        return neighbors

    def find_sortest_path(self, data: list, source: tuple, target: tuple):
        seen = [source]
        todo = [(manhattan_distance(source, target), source, 0)]
        while len(todo) != 0:
            _, coord, steps = todo.pop(0)
            if coord == target:
                return steps
            for neighbor in self.find_neighbors(data, coord):
                if neighbor not in seen:
                    # print(f"Add {neighbor} from {coord}")
                    seen.append(neighbor)
                    todo.append((manhattan_distance(neighbor, target) + steps, neighbor, steps+1))
                    todo.sort(key=lambda x: (x[0], x[2]))

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        # Coordinates: (ROW, COLUMN)
        source = [(i, row.index(-13)) for i, row in enumerate(data) if -13 in row][0]
        target = [(i, row.index(99)) for i, row in enumerate(data) if 99 in row][0]
        data[source[0]][source[1]] = 1
        data[target[0]][target[1]] = 26
        shortest_path = 99999
        sources = [[(i, j) for j, value in enumerate(row) if value == 1] for i, row in enumerate(data) if 1 in row]
        sources = list(itertools.chain.from_iterable(sources))
        for source in sources:
            path = self.find_sortest_path(data, source, target)
            if path is None:
                continue
            shortest_path = path if path < shortest_path else shortest_path
        return shortest_path


if __name__ == "__main__":
    # Load task
    t = Task12()

    # Run task
    t.run_all()
