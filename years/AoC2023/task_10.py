from utils.decorators import timer, debug_shape
from utils.task import Task


class Task10(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 10

    def preprocess(self, data: list) -> dict:
        new_data = {}
        for i, line in enumerate(data):
            new_data[i] = {j: char for j, char in enumerate(line)}
        return new_data

    @staticmethod
    def find_start(data: dict) -> tuple:
        for i, line in data.items():
            for j, char in line.items():
                if char == "S":
                    return i, j

    @staticmethod
    def get_neighbors(data: dict, pos: tuple) -> list:
        neighbors = []
        if pos[0] + 1 in data and pos[1] + 1 in data[pos[0] + 1]:
            neighbors.append((pos[0] + 1, pos[1] + 1))
        if pos[0] + 1 in data and pos[1] - 1 in data[pos[0] + 1]:
            neighbors.append((pos[0] + 1, pos[1] - 1))
        if pos[0] - 1 in data and pos[1] + 1 in data[pos[0] - 1]:
            neighbors.append((pos[0] - 1, pos[1] + 1))
        if pos[0] - 1 in data and pos[1] - 1 in data[pos[0] - 1]:
            neighbors.append((pos[0] - 1, pos[1] - 1))
        return neighbors

    @staticmethod
    def find_neighbors(data: dict, pos: tuple) -> list:
        if pos[0] not in data or pos[1] not in data[pos[0]]:
            raise ValueError("Node is not in loop")
        char = data[pos[0]][pos[1]]
        if char == "|":
            # print(f"Found | at {pos}")
            return [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1])]
        if char == "-":
            # print(f"Found - at {pos}")
            return [(pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        if char == "L":
            # print(f"Found L at {pos}")
            return [(pos[0] - 1, pos[1]), (pos[0], pos[1] + 1)]
        if char == "F":
            # print(f"Found F at {pos}")
            return [(pos[0] + 1, pos[1]), (pos[0], pos[1] + 1)]
        if char == "J":
            # print(f"Found J at {pos}")
            return [(pos[0] - 1, pos[1]), (pos[0], pos[1] - 1)]
        if char == "7":
            # print(f"Found 7 at {pos}")
            return [(pos[0] + 1, pos[1]), (pos[0], pos[1] - 1)]
        raise ValueError("Symbol not recognized")

    @staticmethod
    def find_neighbors_of_start(data: dict, start: tuple) -> list:
        neighbors = []
        if start[0] + 1 in data and start[1] in data[start[0] + 1]:
            if data[start[0] + 1][start[1]] in ["|", "7", "F"]:
                neighbors.append((start[0] + 1, start[1]))
        if start[0] - 1 in data and start[1] in data[start[0] - 1]:
            if data[start[0] - 1][start[1]] in ["|", "J", "L"]:
                neighbors.append((start[0] - 1, start[1]))
        if start[0] in data and start[1] + 1 in data[start[0]]:
            if data[start[0]][start[1] + 1] in ["-", "7", "J"]:
                neighbors.append((start[0], start[1] + 1))
        if start[0] in data and start[1] - 1 in data[start[0]]:
            if data[start[0]][start[1] - 1] in ["-", "L", "F"]:
                neighbors.append((start[0], start[1] - 1))
        return neighbors

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: dict) -> int:
        start = self.find_start(data)
        left, right = self.find_neighbors_of_start(data, start)
        left_loop = [start, left]
        right_loop = [start, right]
        i = 1
        # Loop from both sides until it converges to the same point
        while left_loop[-1] != right_loop[-1]:
            next_left = self.find_neighbors(data, left_loop[-1])
            next_right = self.find_neighbors(data, right_loop[-1])
            for n in next_left:
                if n not in left_loop:
                    left_loop.append(n)
            for n in next_right:
                if n not in right_loop:
                    right_loop.append(n)
            i += 1
        return i

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: dict) -> int:
        # Find the loop
        start = self.find_start(data)
        start_neighbor = self.find_neighbors_of_start(data, start)
        loop_tiles = [start, start_neighbor[0]]
        tile = start_neighbor[0]
        while tile != start_neighbor[1]:
            next_tile = self.find_neighbors(data, tile)
            for n in next_tile:
                if n not in loop_tiles:
                    loop_tiles.append(n)
                    tile = n
        # Find enclosures
        left_side = []
        right_side = []
        for i, tile in enumerate(loop_tiles):
            if i + 1 >= len(loop_tiles):
                break
            direction = (loop_tiles[i + 1][0] - tile[0], loop_tiles[i + 1][1] - tile[1])
            left = (tile[0] - direction[1], tile[1] + direction[0])
            if left not in loop_tiles and left not in left_side:
                left_side.append(left)
            right = (tile[0] + direction[1], tile[1] - direction[0])
            if right not in loop_tiles and right not in right_side:
                right_side.append(right)
            behind = (tile[0] - direction[0], tile[1] - direction[1])
            if behind not in loop_tiles:
                previous = loop_tiles[i-1]
                previous_direction = (tile[0] - previous[0], tile[1] - previous[1])
                # If the current tile curves left, behind = right; if curves right, behind is left
                if direction == (previous_direction[1], -previous_direction[0]):
                    # Curves right
                    if behind not in left_side:
                        left_side.append(behind)
                else:
                    # Curves left
                    if behind not in right_side:
                        right_side.append(behind)
        # The outside will contain negative numbers, the inside will not
        if any(value[0] < 0 or value[1] < 0 for value in left_side):
            # Right side is inside; Do BFS to ensure all have been found
            for pos in right_side:
                right_side = self.bfs(data, pos, right_side, loop_tiles)
            enclosed_tiles = right_side
        else:
            # Left side is inside; Do BFS to ensure all have been found
            for pos in left_side:
                left_side = self.bfs(data, pos, left_side, loop_tiles)
            enclosed_tiles = left_side
        return len(enclosed_tiles)

    def bfs(self, data: dict, pos: tuple, seen: list, loop: list):
        # Find connected, unseen tiles
        queue = [pos]
        while len(queue) != 0:
            coord = queue.pop()
            neighbors = self.get_neighbors(data, coord)
            for n in neighbors:
                if n in seen or n in loop:
                    continue
                queue.append(n)
                seen.append(n)
        return seen


if __name__ == "__main__":
    # Load task
    t = Task10()

    # Run task
    t.run_all()
