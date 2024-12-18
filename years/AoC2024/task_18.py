import bisect

from utils.decorators import timer, debug
from utils.task import Task


class Task18(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 18

    def preprocess(self, data: list) -> list:
        return [tuple([int(num) for num in line.split(',')]) for line in data]

    @staticmethod
    def find_neighbors(pos: tuple, area: dict, max_size: int) -> list:
        neighbors = []
        x, y = pos
        if x > 0 and (x - 1, y) not in area:
            neighbors.append((x - 1, y))
        if y > 0 and (x, y - 1) not in area:
            neighbors.append((x, y - 1))
        if x < max_size and (x + 1, y) not in area:
            neighbors.append((x + 1, y))
        if y < max_size and (x, y + 1) not in area:
            neighbors.append((x, y + 1))
        return neighbors

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        max_grid_size = 70 if len(data) > 100 else 6
        max_steps = 1024 if len(data) > 100 else 12
        fallen = {pos: True for pos in data[:max_steps]}
        return self.find_exit(fallen, max_grid_size)

    def find_exit(self, fallen: dict, max_grid_size: int):
        end_pos = (max_grid_size, max_grid_size)
        seen = {}
        todo = [((0, 0), 0)]
        while len(todo) > 0:
            pos, current_score = todo.pop(0)
            if pos == end_pos:
                return current_score
            for neighbor in self.find_neighbors(pos, fallen, max_grid_size):
                if neighbor in seen:
                    continue
                seen[neighbor] = True
                bisect.insort(todo, (neighbor, current_score + 1), key=lambda x: x[1])
        return 0

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> str:
        max_grid_size = 70 if len(data) > 100 else 6
        fallen = {}
        for max_steps in range(len(data)):
            fallen[data[max_steps]] = True
            if self.find_exit(fallen, max_grid_size) == 0:
                return f"{data[max_steps][0]},{data[max_steps][1]}"


if __name__ == "__main__":
    # Load task
    t = Task18()

    # Run task
    t.run_all()
