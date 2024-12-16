import bisect

from utils.decorators import timer, debug_shape
from utils.task import Task


class Task16(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 16

    def preprocess(self, data: list) -> list:
        return [[char for char in line] for line in data]

    @staticmethod
    def find_character(maze: list, to_find: str) -> tuple:
        for i, line in enumerate(maze):
            for j, char in enumerate(line):
                if char == to_find:
                    return i, j

    @staticmethod
    def find_neighbors(maze: list, pos: tuple, direction: tuple) -> list:
        neighbors = []
        if maze[pos[0] + direction[0]][pos[1] + direction[1]] != "#":
            neighbors.append(((pos[0] + direction[0], pos[1] + direction[1]), 1, direction))
        if maze[pos[0] + direction[1]][pos[1] + direction[0]] != "#":
            neighbors.append(((pos[0] + direction[1], pos[1] + direction[0]), 1001, (direction[1], direction[0])))
        if maze[pos[0] - direction[1]][pos[1] - direction[0]] != "#":
            neighbors.append(((pos[0] - direction[1], pos[1] - direction[0]), 1001, (-direction[1], -direction[0])))
        return neighbors

    def find_best_path(self, maze: list, start_pos: tuple, start_direct: tuple, end_pos: tuple):
        seen = {}
        todo = [(start_pos, start_direct, 0)]
        best_score = None
        while len(todo) > 0:
            pos, direction, current_score = todo.pop(0)
            if best_score is not None and current_score > best_score:
                break
            if pos == end_pos:
                best_score = current_score
            for neighbor, score_cost, new_direction in self.find_neighbors(maze, pos, direction):
                if (neighbor, new_direction) in seen and current_score + score_cost >= seen[neighbor, new_direction]:
                    continue
                seen[neighbor, new_direction] = current_score + score_cost
                bisect.insort(todo, (neighbor, new_direction, current_score + score_cost), key=lambda x: x[2])
        return best_score if best_score is not None else 0

    def find_best_paths(self, maze: list, start_pos: tuple, start_direct: tuple, end_pos: tuple):
        seen = {}
        todo = [(start_pos, start_direct, 0, [start_pos])]
        end_directions = []
        end_paths = []
        best_score = None
        while len(todo) > 0:
            pos, direction, current_score, path = todo.pop(0)
            if best_score is not None and current_score > best_score:
                break
            if pos == end_pos:
                best_score = current_score
                end_directions.append(direction)
                end_paths.append(path)
            for neighbor, score_cost, new_direction in self.find_neighbors(maze, pos, direction):
                if (neighbor, new_direction) in seen and current_score + score_cost > seen[neighbor, new_direction]:
                    continue
                seen[neighbor, new_direction] = current_score + score_cost
                new_path = path.copy()
                new_path.append(neighbor)
                bisect.insort(todo, (neighbor, new_direction, current_score + score_cost, new_path), key=lambda x: x[2])
        return best_score if best_score is not None else 0, end_paths

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        start_pos = self.find_character(data, "S")
        start_direct = (0, 1)
        end_pos = self.find_character(data, "E")
        return self.find_best_path(data, start_pos, start_direct, end_pos)

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        start_pos = self.find_character(data, "S")
        start_direct = (0, 1)
        end_pos = self.find_character(data, "E")
        _, end_paths = self.find_best_paths(data, start_pos, start_direct, end_pos)
        seats = []
        for path in end_paths:
            for tile in path:
                if tile not in seats:
                    seats.append(tile)
        return len(seats)


if __name__ == "__main__":
    # Load task
    t = Task16()

    # Run task
    t.run_all()
