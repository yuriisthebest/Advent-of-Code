import bisect

from utils.decorators import timer, debug_shape
from utils.task import Task


class Task20(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 20

    def preprocess(self, data: list) -> list:
        return [[char for char in line] for line in data]

    @staticmethod
    def find_char(data: list, key: chr) -> tuple:
        for i, line in enumerate(data):
            for j, char in enumerate(line):
                if char == key:
                    return i, j

    @staticmethod
    def find_neighbors(data: list, pos: tuple, cheated: list) -> list:
        neighbors = []
        i, j = pos
        if i > 0 and (data[i - 1][j] != "#" or (i - 1, j) in cheated):
            neighbors.append((i - 1, j))
        if j > 0 and (data[i][j - 1] != "#" or (i, j - 1) in cheated):
            neighbors.append((i, j - 1))
        if i < len(data) - 1 and (data[i + 1][j] != "#" or (i + 1, j) in cheated):
            neighbors.append((i + 1, j))
        if j < len(data[0]) - 1 and (data[i][j + 1] != "#" or (i, j + 1) in cheated):
            neighbors.append((i, j + 1))
        return neighbors

    @staticmethod
    def get_value(data: list, i: int, j: int) -> chr:
        try:
            return data[i][j]
        except IndexError:
            return "#"

    def smart_cheat(self, data: list, pos: tuple) -> list:
        # Find usefull cheats in the current position. Any position can have 4 different cheats
        i, j = pos
        cheats = []
        if (self.get_value(data, i + 2, j - 1) != "#"
                or self.get_value(data, i + 3, j) != "#"
                or self.get_value(data, i + 2, j + 1) != "#"):
            cheats.append([(i + 1, j), (i + 2, j)])
        if (self.get_value(data, i - 2, j - 1) != "#"
                or self.get_value(data, i - 3, j) != "#"
                or self.get_value(data, i - 2, j + 1) != "#"):
            cheats.append([(i - 1, j), (i - 2, j)])
        if (self.get_value(data, i - 1, j + 2) != "#"
                or self.get_value(data, i, j + 3) != "#"
                or self.get_value(data, i + 1, j + 2) != "#"):
            cheats.append([(i, j + 1), (i, j + 2)])
        if (self.get_value(data, i - 1, j - 2) != "#"
                or self.get_value(data, i, j - 3) != "#"
                or self.get_value(data, i + 1, j - 2) != "#"):
            cheats.append([(i, j - 1), (i, j - 2)])
        return cheats

    def find_paths(self, data: list, start: tuple, end: tuple, max_cheats: int = 0) -> list:
        seen = [(start, [])]
        todo = [(start, 0, [])]
        endings = []
        while len(todo) > 0:
            # print(todo)
            pos, current_score, cheated = todo.pop(0)
            # print(f"Next: {pos}, {current_score}, {cheated}, {data[pos[0]][pos[1]]}")
            if pos == end:
                endings.append(current_score)
                if len(cheated) == 0:
                    return endings
            # Make steps
            if len(cheated) != 1:
                for neighbor in self.find_neighbors(data, pos, cheated):
                    if (neighbor, cheated) in seen:
                        continue
                    seen.append((neighbor, cheated))
                    bisect.insort(todo, (neighbor, current_score + 1, cheated), key=lambda x: x[1])
                    # print(f"Added: {neighbor, current_score + 1, cheated}")
            # Generated cheated moves
            if len(cheated) < max_cheats:
                # cheats = self.smart_cheat(data, pos)
                # for cheat in cheats:
                #     bisect.insort(todo, (pos, current_score, cheat), key=lambda x: x[1])
                for neighbor in self.find_neighbors(data, pos, True):
                    if len(cheated) + 1 == max_cheats and data[neighbor[0]][neighbor[1]] == "#":
                        continue
                    pre_cheated = cheated.copy()
                    pre_cheated.append(neighbor)
                    if (neighbor, pre_cheated) in seen:
                        continue
                    seen.append((neighbor, pre_cheated))
                    bisect.insort(todo, (neighbor, current_score + 1, pre_cheated), key=lambda x: x[1])
                print(f"Added: {neighbor, current_score + 1, pre_cheated}")

    def get_path(self, data: list, start: tuple, end: tuple) -> list:
        seen = [start]
        todo = [(start, 0)]
        while len(todo) > 0:
            pos, current_score = todo.pop(0)
            if pos == end:
                return seen
            # Make steps
            for neighbor in self.find_neighbors(data, pos, []):
                if neighbor in seen:
                    continue
                seen.append(neighbor)
                bisect.insort(todo, (neighbor, current_score + 1), key=lambda x: x[1])

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        start = self.find_char(data, "S")
        end = self.find_char(data, "E")
        path = self.get_path(data, start, end)
        num_large_skips = 0
        for i, pos in enumerate(path):
            for skip in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                new_pos = (pos[0] + skip[0], pos[1] + skip[1])
                if self.get_value(data, *new_pos) != "#" and new_pos in path and path.index(new_pos) > i + 100:
                    num_large_skips += 1
        return num_large_skips

    @staticmethod
    def manhattan_distance(pos1: tuple, pos2: tuple) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        save_threshold = 100 if len(data) > 100 else 50
        start = self.find_char(data, "S")
        end = self.find_char(data, "E")
        path = self.get_path(data, start, end)
        num_large_skips = 0
        for i, cheat_start in enumerate(path):
            for j, cheat_end in enumerate(path):
                # Time optimization by checking this once before calculating the manhattan distance
                if j < i + save_threshold:
                    continue
                if (cheat_time := self.manhattan_distance(cheat_start, cheat_end)) > 20:
                    continue
                if j < i + save_threshold + cheat_time:
                    continue
                num_large_skips += 1
        return num_large_skips


if __name__ == "__main__":
    # Load task
    t = Task20()

    # Run task
    t.run_all()
