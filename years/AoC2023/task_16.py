from utils.decorators import timer, debug
from utils.task import Task


class Task16(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 16

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        to_process = [((0, 0), (0, 1))]
        energized = self.run_beam(data, to_process)
        return len(energized)

    def run_beam(self, data: list, to_process: list):
        energized = []
        while len(to_process) != 0:
            tile, direction = to_process.pop()
            energized.append((tile, direction))
            new_tiles = self.process_tile(data, tile, direction)
            for tile, direction in new_tiles:
                if tile[0] < 0 or tile[0] >= len(data) or tile[1] < 0 or tile[1] >= len(data[tile[0]]):
                    continue
                if (tile, direction) in energized:
                    continue
                to_process.append((tile, direction))
        energized = set([e[0] for e in energized])
        return energized

    @staticmethod
    def process_tile(data: list, tile: tuple, from_direction: tuple) -> list:
        # Process tile
        if data[tile[0]][tile[1]] == "/":
            # Change directions
            new_direction = (-from_direction[1], -from_direction[0])
            new_tile = (tile[0] + new_direction[0], tile[1] + new_direction[1])
            return [(new_tile, new_direction)]
        elif data[tile[0]][tile[1]] == "\\":
            # Change directions
            new_direction = (from_direction[1], from_direction[0])
            new_tile = (tile[0] + new_direction[0], tile[1] + new_direction[1])
            return [(new_tile, new_direction)]
        elif data[tile[0]][tile[1]] == "|" and from_direction in [(0, 1), (0, -1)]:
            # Split vertically
            return [((tile[0] + direct[0], tile[1] + direct[1]), direct) for direct in [(1, 0), (-1, 0)]]
        elif data[tile[0]][tile[1]] == "-" and from_direction in [(1, 0), (-1, 0)]:
            # Split horizontally
            return [((tile[0] + direct[0], tile[1] + direct[1]), direct) for direct in [(0, 1), (0, -1)]]
        else:
            # Continue going in the current direction
            new_tile = (tile[0] + from_direction[0], tile[1] + from_direction[1])
            return [(new_tile, from_direction)]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        max_energized = 0
        potential_starts = [((0, 0), (0, 1))]
        for i in range(len(data)):
            potential_starts.append(((i, 0), (0, 1)))
            potential_starts.append(((i, len(data) - 1), (0, -1)))
        for i in range(len(data[0])):
            potential_starts.append(((0, i), (1, 0)))
            potential_starts.append(((len(data) - 1, i), (-1, 0)))
        for start in potential_starts:
            num_energized = len(self.run_beam(data, [start]))
            if num_energized > max_energized:
                max_energized = num_energized
        return max_energized


if __name__ == "__main__":
    # Load task
    t = Task16()

    # Run task
    t.run_all()
