from utils.decorators import timer, debug
from utils.task import Task


class Task14(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 14

    def preprocess(self, data: list) -> dict:
        cave = {}
        data = [[tuple(map(int, coord.split(","))) for coord in line if coord != "->"] for line in data]
        for line in data:
            prev_coord = None
            for i, coord in enumerate(line):
                # Skip first coord
                if prev_coord is None:
                    prev_coord = coord
                    continue
                rocks = [(x, y)
                         for x in range(min(coord[0], prev_coord[0]), max(coord[0], prev_coord[0]) + 1)
                         for y in range(min(coord[1], prev_coord[1]), max(coord[1], prev_coord[1]) + 1)]
                for rock in rocks:
                    if rock[1] not in cave:
                        cave[rock[1]] = []
                    if rock[0] not in cave[rock[1]]:
                        cave[rock[1]].append(rock[0])
                # Set prev for next iteration
                prev_coord = coord
        return cave

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: dict) -> int:
        source = (500, 0)
        placed = 0
        while True:
            sand = self.place_sand(data, source)
            if sand is None:
                break
            if sand[1] not in data:
                data[sand[1]] = []
            data[sand[1]].append(sand[0])
            placed += 1
        return placed

    def place_sand(self, cave: dict, source: tuple, bottom: int = 1000):
        if source[1] >= 400:
            return None
        if source[1] + 1 == bottom:
            return source
        for i in [0, -1, +1]:
            if source[1] + 1 not in cave or source[0] + i not in cave[source[1] + 1]:
                return self.place_sand(cave, (source[0] + i, source[1] + 1), bottom)
        return source

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: dict) -> int:
        # Find bottom
        bottom = max(data) + 2
        source = (500, 0)
        placed = 0
        while True:
            sand = self.place_sand(data, source, bottom)
            placed += 1
            if sand is source:
                break
            if sand[1] not in data:
                data[sand[1]] = []
            data[sand[1]].append(sand[0])
        return placed


if __name__ == "__main__":
    # Load task
    t = Task14()

    # Run task
    t.run_all()
