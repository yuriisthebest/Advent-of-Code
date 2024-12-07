from utils.decorators import timer, debug
from utils.task import Task

ROTATIONS = {(-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0)}


class Task6(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 6

    @staticmethod
    def find_start(data) -> tuple:
        for i, line in enumerate(data):
            for j, char in enumerate(line):
                if char in ["<", ">", "v", "^"]:
                    return i, j

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        i, j = self.find_start(data)
        # Assume start position is "^"
        direction = (-1, 0)
        seen = [(i, j)]
        while 0 <= i + direction[0] < len(data) and 0 <= j + direction[1] < len(data[0]):
            # Check if step is obstructed
            if data[i + direction[0]][j + direction[1]] == "#":
                # Rotate
                direction = ROTATIONS[direction]
            else:
                i += direction[0]
                j += direction[1]
                if (i, j) not in seen:
                    seen.append((i, j))
        return len(seen)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        obstruction_locations = []
        start_i, start_j = self.find_start(data)
        max_height, max_width = len(data), len(data[0])
        i, j = start_i, start_j
        # Assume start position is "^"
        direction = (-1, 0)
        seen = [(i, j, direction)]
        while 0 <= i + direction[0] < max_height and 0 <= j + direction[1] < max_width:
            # Check if step is obstructed
            if data[i + direction[0]][j + direction[1]] == "#":
                # Rotate
                direction = ROTATIONS[direction]
            else:
                # Check if moving to the right would cause a loop
                if data[i + direction[0]][j + direction[1]] != "^":
                    new_data = data.copy()
                    new_line = list(new_data[i + direction[0]])
                    new_line[j + direction[1]] = "#"
                    new_data[i + direction[0]] = "".join(new_line)
                    if self.returns_to_self(new_data, start_i, start_j, (-1, 0), max_height, max_width):
                        if (i + direction[0], j + direction[1]) not in obstruction_locations:
                            obstruction_locations.append((i + direction[0], j + direction[1]))
                # Take a step
                i += direction[0]
                j += direction[1]
                if (i, j) not in seen:
                    seen.append((i, j, direction))
        return len(obstruction_locations)

    @staticmethod
    def returns_to_self(data: list, i: int, j: int, direction: tuple, max_height: int, max_width: int) -> bool:
        seen = [(i, j, direction)]
        while 0 <= i + direction[0] < max_height and 0 <= j + direction[1] < max_width:
            # Check if step is obstructed
            if data[i + direction[0]][j + direction[1]] == "#":
                # Rotate
                direction = ROTATIONS[direction]
            else:
                i += direction[0]
                j += direction[1]
                if (i, j, direction) in seen:
                    return True
                seen.append((i, j, direction))
        return False


if __name__ == "__main__":
    # Load task
    t = Task6()

    # Run task
    t.run_all()
