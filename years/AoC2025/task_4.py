from utils.decorators import timer, debug_shape
from utils.task import Task
from utils.data_structures.grid import Grid


class Task4(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 4

    def preprocess(self, data: list) -> Grid:
        return Grid(data, edge_included=False)

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: Grid) -> int:
        result = 0
        for cell in data.get_each_cells():
            if cell.get("value") != "@":
                continue
            adjacents = data.get_adjacent(cell, ortogonal=False, allow={"value": "@"})
            if len(adjacents) < 4:
                result += 1
        return result

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: Grid) -> int:
        result = 0
        changed = True
        while changed:
            changed = False
            for cell in data.get_each_cells():
                if cell.get("value") != "@":
                    continue
                adjacents = data.get_adjacent(cell, ortogonal=False, allow={"value": "@"})
                if len(adjacents) < 4:
                    cell.update_tag({"value": "."})
                    result += 1
                    changed = True
        return result


if __name__ == "__main__":
    # Load task
    t = Task4()

    # Run task
    t.run_all()
