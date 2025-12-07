from utils.decorators import timer, debug_shape
from utils.task import Task
from utils.data_structures.grid import Grid


class Task7(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 7

    def preprocess(self, data: list) -> Grid:
        return Grid(data)

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: Grid) -> int:
        splits = 0
        start = data.find_values(values=["S"])
        # Keep track of current beams
        beams = [start]
        # Evolve from the top-down step by step
        for i in range(data.max_dims[0] - 1):
            new_beams = []
            for beam in beams:
                pos = beam.get_pos()
                if data.get_cell((pos[0] + 1, pos[1])).get("value") == "^":
                    # Always count the split if the splitter gets hit, no matter if it actually adds a beam
                    splits += 1
                    left_cell = data.get_cell((pos[0], pos[1] - 1)) if data.contains_cell(
                        (pos[0], pos[1] - 1)) else None
                    right_cell = data.get_cell((pos[0], pos[1] + 1)) if data.contains_cell(
                        (pos[0], pos[1] + 1)) else None
                    # Only split if there is not a beam continuing from above or another has already been generated
                    if left_cell is not None and left_cell not in beams and data.get_cell(
                            (pos[0] + 1, pos[1] - 1)) not in new_beams:
                        new_beams.append(data.get_cell((pos[0] + 1, pos[1] - 1)))
                    # Only split if there is not a beam continuing from above or another has already been generated
                    if right_cell is not None and right_cell not in beams and data.get_cell(
                            (pos[0] + 1, pos[1] + 1)) not in new_beams:
                        new_beams.append(data.get_cell((pos[0] + 1, pos[1] + 1)))
                # Continue the beam without splitting
                elif data.contains_cell((pos[0] + 1, pos[1])):
                    new_beams.append(data.get_cell((pos[0] + 1, pos[1])))
            beams = new_beams
        return splits

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: Grid) -> int:
        start = data.find_values(values=["S"])
        # Keep track of the amount of timelines that reach a certain beam
        beams = {start: 1}
        for i in range(data.max_dims[0] - 1):
            new_beams = {}
            for beam, count in beams.items():
                pos = beam.get_pos()
                if data.get_cell((pos[0] + 1, pos[1])).get("value") == "^":
                    # Split left
                    if data.get_cell((pos[0] + 1, pos[1] - 1)) not in new_beams:
                        new_beams[data.get_cell((pos[0] + 1, pos[1] - 1))] = count
                    else:
                        new_beams[data.get_cell((pos[0] + 1, pos[1] - 1))] += count
                    # Split right
                    if data.get_cell((pos[0] + 1, pos[1] + 1)) not in new_beams:
                        new_beams[data.get_cell((pos[0] + 1, pos[1] + 1))] = count
                    else:
                        new_beams[data.get_cell((pos[0] + 1, pos[1] + 1))] += count
                # Continue the beam
                elif data.contains_cell((pos[0] + 1, pos[1])):
                    if data.get_cell((pos[0] + 1, pos[1])) not in new_beams:
                        new_beams[data.get_cell((pos[0] + 1, pos[1]))] = count
                    else:
                        new_beams[data.get_cell((pos[0] + 1, pos[1]))] += count
            beams = new_beams
        return sum(beams.values())


if __name__ == "__main__":
    # Load task
    t = Task7()

    # Run task
    t.run_all()
