from utils.decorators import timer, debug
from utils.task import Task


def manhattan_distance(point1_x: int, point1_y: int, point2_x: int, point2_y: int) -> int:
    return abs(point1_x - point2_x) + abs(point1_y - point2_y)


class Task15(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 15

    def preprocess(self, data: list) -> list:
        # Sensor X, Sensor Y, Beacon X, Beacon Y
        return [[int(line[2][2:-1]), int(line[3][2:-1]), int(line[8][2:-1]), int(line[9][2:])] for line in data]

    def run_part_1(self):
        # Run part 1
        test1 = self.part_1(self.test, 10)
        task1 = self.part_1(self.task, 2000000) if not self.TEST_MODE else None
        return test1, task1

    def run_part_2(self):
        # Run part 2
        test2 = self.part_2(self.test, 20)
        task2 = self.part_2(self.task, 4000000) if not self.TEST_MODE else None
        return test2, task2

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list, height_to_check: int) -> int:
        distances = [manhattan_distance(*sensor) for sensor in data]
        result = self.check_line(data, distances, height_to_check)
        return len(result)

    @staticmethod
    def check_line(sensors: list, distances: list, height: int) -> list:
        within_range = []
        min_sensor_x = min([sensor[0] - distance for sensor, distance in zip(sensors, distances)])
        max_sensor_x = max([sensor[0] + distance for sensor, distance in zip(sensors, distances)])
        for i in range(min_sensor_x, max_sensor_x):
            for sensor, distance in zip(sensors, distances):
                if sensor[2] == i and sensor[3] == height:
                    continue
                if manhattan_distance(sensor[0], sensor[1], i, height) <= distance:
                    within_range.append(i)
                    break
        return within_range

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list, max_dims: int) -> int:
        # Only 1 cell is empty within the search range, thus only check cells just outside sensors range
        distances = [manhattan_distance(*sensor) for sensor in data]
        for sensor, distance in zip(data, distances):
            for location in ringscan(sensor[0], sensor[1], distance + 1, distance + 1):
                # Check if location is within scope
                if 0 > location[0] or location[0] > max_dims:
                    continue
                if 0 > location[1] or location[1] > max_dims:
                    continue
                # Check if location is covered by sensor
                for sensor2, distance2 in zip(data, distances):
                    if manhattan_distance(sensor2[0], sensor2[1], location[0], location[1]) <= distance2:
                        break
                else:
                    return 4000000 * location[0] + location[1]

    @staticmethod
    @timer(YEAR, TASK_NUM)
    def sensor_covered_places(sensor: list, covered: dict) -> dict:
        distance = manhattan_distance(*sensor)
        for y in range(-distance, distance + 1):
            for x in range(-distance, distance + 1):
                if sensor[0] + y not in covered:
                    covered[sensor[0] + y] = []
                if sensor[1] + x not in covered[sensor[0] + y]:
                    covered[sensor[0] + y].append(sensor[1] + x)
        return covered


# IMPORTED CODE
def manhattan(point1, point2):
    """Computes distance between 2D points using manhattan metric
    :param point1: 1st point
    :type point1: list
    :param point2: 2nd point
    :type point2: list
    :returns: Distance between point1 and point2
    :rtype: float
    """

    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


# IMPORTED CODE
def ringscan(x0, y0, r1, r2, metric=manhattan):
    """Scan pixels in a ring pattern around a center point clockwise
    :param x0: Center x-coordinate
    :type x0: int
    :param y0: Center y-coordinate
    :type y0: int
    :param r1: Initial radius
    :type r1: int
    :param r2: Final radius
    :type r2: int
    :param metric: Distance metric
    :type metric: function
    :returns: Coordinate generator
    :rtype: function
    """

    # Validate inputs
    if r1 < 0:
        raise ValueError("Initial radius must be non-negative")
    if r2 < 0:
        raise ValueError("Final radius must be non-negative")
    if not hasattr(metric, "__call__"):
        raise TypeError("Metric not callable")

    # Define clockwise step directions
    direction = 0
    steps = {0: [1, 0],
             1: [1, -1],
             2: [0, -1],
             3: [-1, -1],
             4: [-1, 0],
             5: [-1, 1],
             6: [0, 1],
             7: [1, 1]}
    nsteps = len(steps)

    center = [x0, y0]

    # Scan distances outward (1) or inward (-1)
    rstep = 1 if r2 >= r1 else -1
    for distance in range(r1, r2 + rstep, rstep):

        initial = [x0, y0 + distance]
        current = initial

        # Number of tries to find a valid neighrbor
        ntrys = 0

        while True:

            # Short-circuit special case
            if distance == 0:
                yield current[0], current[1]
                break

            # Try and take a step and check if still within distance
            nextpoint = [current[i] + steps[direction][i] for i in range(2)]
            if metric(center, nextpoint) != distance:

                # Check if we tried all step directions and failed
                ntrys += 1
                if ntrys == nsteps:
                    break

                # Try the next direction
                direction = (direction + 1) % nsteps
                continue

            ntrys = 0
            yield current[0], current[1]

            # Check if we have come all the way around
            current = nextpoint
            if current == initial:
                break

        # Check if we tried all step directions and failed
        if ntrys == nsteps:
            break


if __name__ == "__main__":
    # Load task
    t = Task15()

    # Run task
    t.run_all()
