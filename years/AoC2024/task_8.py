from utils.decorators import timer, debug
from utils.task import Task


class Task8(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 8

    def preprocess(self, data: list) -> list:
        height = len(data)
        width = len(data[0])
        antennas = {}
        for i, line in enumerate(data):
            for j, char in enumerate(line):
                if char != ".":
                    if char not in antennas:
                        antennas[char] = []
                    antennas[char].append((i, j))
        return [height, width, antennas]

    @staticmethod
    def antinode_locations(antennas: list) -> list:
        locations = []
        for y, x in antennas:
            for i, j in antennas:
                if (y, x) == (i, j):
                    continue
                # Antenna 1 is always above, or on equal height, as antenna 2
                antenna1 = (y, x) if y <= i else (i, j)
                antenna2 = (y, x) if antenna1 == (i, j) else (i, j)

                if antenna1[1] <= antenna2[1]:
                    pos1 = (min(y, i) - abs(y - i), min(x, j) - abs(x - j))
                    pos2 = (max(y, i) + abs(y - i), max(x, j) + abs(x - j))
                else:
                    pos1 = (min(y, i) - abs(y - i), max(x, j) + abs(x - j))
                    pos2 = (max(y, i) + abs(y - i), min(x, j) - abs(x - j))
                if pos1 not in locations:
                    locations.append(pos1)
                if pos2 not in locations:
                    locations.append(pos2)
        return locations

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        total = []
        height, width = data[0], data[1]
        for antenna_type in data[2]:
            locations = self.antinode_locations(data[2][antenna_type])
            for i, j in locations:
                if 0 <= i < height and 0 <= j < width:
                    if (i, j) not in total:
                        total.append((i, j))
        return len(total)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        total = []
        for antenna_type in data[2]:
            locations = self.harmonic_locations(data[2][antenna_type], data[0], data[1])
            for i, j in locations:
                if (i, j) not in total:
                    total.append((i, j))
        print(total)
        return len(total)

    @staticmethod
    def harmonic_locations(antennas: list, height: int, width: int) -> list:
        locations = []
        for y, x in antennas:
            for i, j in antennas:
                if (y, x) == (i, j):
                    continue
                # Antenna 1 is always above, or on equal height, as antenna 2
                antenna1 = (y, x) if y <= i else (i, j)
                antenna2 = (y, x) if antenna1 == (i, j) else (i, j)
                y_diff = antenna2[0] - antenna1[0]
                x_diff = antenna2[1] - antenna1[1]
                loc_height = antenna1[0] - y_diff * (antenna1[0] // y_diff) if y_diff != 0 else antenna1[0]
                loc_width = antenna1[1] - x_diff * (antenna1[0] // y_diff) if y_diff != 0 else antenna1[1] - x_diff * (
                        antenna1[1] // x_diff)
                # If non-valid start, find one
                while not (0 <= loc_height < height and 0 <= loc_width < width):
                    loc_height += y_diff
                    loc_width += x_diff
                while 0 <= loc_height < height and 0 <= loc_width < width:
                    locations.append((loc_height, loc_width))
                    loc_height += y_diff
                    loc_width += x_diff
        return locations


if __name__ == "__main__":
    # Load task
    t = Task8()

    # Run task
    t.run_all()
