from utils.decorators import timer, debug
from utils.task import Task


def produce_line_values(p1: tuple, p2: tuple) -> list:
    """
    Return all values between two points, including the points

    :param p1: Point 1
    :param p2: Point 2
    :return: List of values between the two points
    """
    points = []
    # Horizontal
    if p1[0] == p2[0]:
        large, small = max(p1[1], p2[1]), min(p1[1], p2[1])
        for i in range(small, large + 1):
            points.append((p1[0], i))
        return points
    # Vertical
    if p1[1] == p2[1]:
        large, small = max(p1[0], p2[0]), min(p1[0], p2[0])
        for i in range(small, large + 1):
            points.append((i, p1[1]))
        return points
    # Diagonal
    direction = 0
    if p1[0] < p2[0]:
        direction = 1 if p1[1] < p2[1] else -1
    if p1[0] > p2[0]:
        direction = 1 if p1[1] > p2[1] else -1

    large_x, small_x = max(p1[0], p2[0]), min(p1[0], p2[0])
    large_y, small_y = max(p1[1], p2[1]), min(p1[1], p2[1])
    if direction == -1:
        large_y, small_y = small_y, large_y
    for x, y in zip(range(small_x, large_x + 1), range(small_y, large_y + direction, direction)):
        points.append((x, y))
    return points


class Task5(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 5

    def preprocess(self, data: list) -> list:
        """
        Convert list of strings into list of lines, where each line is represented by their endpoints

        :param data: List of lists, each inner-list contains 3 elements: string point 1, "->", string point 2
        :return: List of the format [ [(p1_x, p1_y), (p2_x, p2_y)], [(p1_x, p1_y), (p2_x, p2_y)], ... ]
        """
        for line in data:
            line.remove("->")
            for i, value in enumerate(line):
                items = value.split(",")
                line[i] = int(items[0]), int(items[1])
        return data

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list, diagonal: bool = False) -> int:
        """
        Count the amount of points where two or more lines overlap

        :param data: A list of lines, each line is represented by their two endpoints
        :param diagonal: Boolean to ignore diagonal points or not
        :return: Number of times two or more lines overlap
        """
        overlaps = 0
        seen = {}
        for i, line in enumerate(data):
            # Ignore non-straight lines
            if line[0][0] != line[1][0] and line[0][1] != line[1][1] and not diagonal:
                continue
            # Add points to be seen
            values = produce_line_values(line[0], line[1])
            for point in values:
                if point in seen:
                    seen[point] += 1
                    if seen[point] == 2:
                        overlaps += 1
                else:
                    seen[point] = 1
        return overlaps

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Count the amount of points where two or more lines overlap, includes diagonal lines

        :param data: A list of lines, each line is represented by their two endpoints
        :return: Number of times two or more lines overlap
        """
        return self.part_1(data, True)


if __name__ == "__main__":
    # Load task
    t = Task5()

    # Run task
    t.run_all()
