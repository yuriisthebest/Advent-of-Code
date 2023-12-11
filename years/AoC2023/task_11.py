from utils.decorators import timer, debug
from utils.task import Task


class Task11(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 11

    @staticmethod
    def manhattan2d(coord1: tuple, coord2: tuple):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        empty_columns, empty_rows, galaxies = self.prepare_data(data)
        return self.calculate_distance(empty_columns, empty_rows, galaxies)

    @staticmethod
    def prepare_data(data):
        empty_rows = [i for i, row in enumerate(data) if row.count("#") == 0]
        empty_columns = [i for i in range(len(data[0]))]
        galaxies = []
        # Find all galaxies
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                if value == "#":
                    galaxies.append((i, j))
                    if j in empty_columns:
                        empty_columns.remove(j)
        return empty_columns, empty_rows, galaxies

    def calculate_distance(self, empty_columns, empty_rows, galaxies, expansion: int = 2):
        total_distance = 0
        # Check every pair of galaxies
        for i, galaxy1 in enumerate(galaxies):
            for galaxy2 in galaxies[i + 1:]:
                regular_distance = self.manhattan2d(galaxy1, galaxy2)
                for expanded in empty_rows:
                    if galaxy1[0] < expanded < galaxy2[0] or galaxy1[0] > expanded > galaxy2[0]:
                        regular_distance += expansion - 1
                for expanded in empty_columns:
                    if galaxy1[1] < expanded < galaxy2[1] or galaxy1[1] > expanded > galaxy2[1]:
                        regular_distance += expansion - 1
                total_distance += regular_distance
        return total_distance

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        empty_columns, empty_rows, galaxies = self.prepare_data(data)
        return self.calculate_distance(empty_columns, empty_rows, galaxies, 1000000)


if __name__ == "__main__":
    # Load task
    t = Task11()

    # Run task
    t.run_all()
