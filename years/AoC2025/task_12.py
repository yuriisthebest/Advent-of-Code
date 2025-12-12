from utils.decorators import timer, debug
from utils.task import Task


class Task12(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 12

    def preprocess(self, data: list) -> tuple:
        presents = []
        regions = []
        for i, line in enumerate(data):
            # Process present
            if line != "" and line[-1] == ":":
                presents.append(tuple(data[i+1:i+4]))
            # Process region
            elif isinstance(line, list):
                regions.append((tuple([int(num) for num in line[0][:-1].split("x")]), [int(num) for num in line[1:]]))
        return presents, regions

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: tuple) -> int:
        fits = 0
        presents, regions = data
        for region in regions:
            if self.check_region(region, tuple(presents)):
                fits += 1
        return fits

    @staticmethod
    def check_region(region: list, shapes: tuple) -> bool:
        size = region[0]
        requirements = tuple(region[1])
        pip_count = [sum([line.count("#") for line in shape]) for shape in shapes]
        total_pips = sum([num_shape * num_pip for num_shape, num_pip in zip(requirements, pip_count)])
        # If the total area of the required shapes is larger than the available area, it's not possible
        return total_pips <= size[0] * size[1]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: tuple) -> int:
        return -1


if __name__ == "__main__":
    # Load task
    t = Task12()

    # Run task
    t.run_all()
