from utils.decorators import timer, debug_shape
from utils.task import Task


class Task12(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 12

    def preprocess(self, data: list) -> list:
        new_data = []
        for line in data:
            new = [char for char in line]
            new.append(".")
            new.insert(0, ".")
            new_data.append(new)
        new_data.append(["." for _ in new_data[0]])
        new_data.insert(0, ["." for _ in new_data[0]])
        return new_data

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        score = 0
        seen = []
        for i, line in enumerate(data):
            for j, char in enumerate(line):
                if data[i][j] == ".":
                    continue
                if (i, j) in seen:
                    continue
                area, neighbors = self.find_area(data, i, j)
                seen.extend(area)
                score += len(area) * len(neighbors)
        return score

    def find_area(self, data: list, i: int, j: int):
        todo = [(i, j)]
        area = [(i, j)]
        neighbors = []
        while len(todo) != 0:
            current_plot = todo.pop()
            for plot, side in self.find_neighbors(data, *current_plot):
                if plot in area:
                    continue
                if data[plot[0]][plot[1]] == data[i][j]:
                    area.append(plot)
                    todo.append(plot)
                else:
                    neighbors.append((plot, side))
        return area, neighbors

    @staticmethod
    def find_neighbors(data: list, i: int, j: int) -> list:
        # Return a list with all neighbors and their relative orientation based on the original plot
        neighbors = []
        if i > 0:
            neighbors.append(((i - 1, j), "top"))
        if j > 0:
            neighbors.append(((i, j - 1), "left"))
        if i < len(data) - 1:
            neighbors.append(((i + 1, j), "bottom"))
        if j < len(data[i]) - 1:
            neighbors.append(((i, j + 1), "right"))
        return neighbors

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        score = 0
        seen = []
        for i, line in enumerate(data):
            for j, char in enumerate(line):
                if data[i][j] == ".":
                    continue
                if (i, j) in seen:
                    continue
                area, neighbors = self.find_area(data, i, j)
                seen.extend(area)
                neighbors = self.condense_neighbors(neighbors)
                score += len(area) * len(neighbors)
        return score

    def condense_neighbors(self, neighbors: list) -> list:
        sides = [[[plot], direction] for plot, direction in neighbors]
        changed = True
        # Try to find two sides which are extentions from each other and thus can be merged
        while changed:
            changed = False
            to_remove = []
            for side, direction in sides:
                found = False
                for side2, direction2 in sides:
                    if side == side2:
                        continue
                    if direction != direction2:
                        continue
                    if any([self.is_next_to(plot1, plot2) for plot1 in side for plot2 in side2]):
                        side.extend(side2)
                        to_remove.append([side2, direction])
                        found = True
                        changed = True
                        break
                if found:
                    break
            for old in to_remove:
                sides.remove(old)
        return sides

    @staticmethod
    def is_next_to(plot: tuple, plot2: tuple):
        if plot[0] == plot2[0] and abs(plot[1] - plot2[1]) <= 1:
            return True
        if plot[1] == plot2[1] and abs(plot[0] - plot2[0]) <= 1:
            return True
        return False


if __name__ == "__main__":
    # Load task
    t = Task12()

    # Run task
    t.run_all()
