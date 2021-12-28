from utils.decorators import timer, debug
from utils.task import Task


def all_orientations():
    orientations = []
    for facing in range(6):
        for rotation in range(4):
            orientations.append((facing, rotation))
    return orientations


def transform_position(pos, orientation, rotation):
    # Credit to SwampThingTom
    pos = orientate(pos, orientation)
    pos = rotate(pos, rotation)
    return pos


def rotate(pos, rotation):
    x, y, z = pos
    if rotation == 0:
        return x, y, z
    elif rotation == 1:
        return z, y, -x
    elif rotation == 2:
        return -x, y, -z
    elif rotation == 3:
        return -z, y, x


def orientate(pos, orientation):
    x, y, z = pos
    if orientation == 0:
        return x, y, z
    elif orientation == 1:
        # (0, -1, 0)
        return x, -y, -z
    elif orientation == 2:
        # (1, 0, 0)
        return y, x, -z
    elif orientation == 3:
        # (-1, 0, 0)
        return y, -x, z
    elif orientation == 4:
        # (0, 0, 1)
        return y, z, x
    elif orientation == 5:
        # (0, 0, -1)
        return y, -z, -x


class Beacon:
    def __init__(self, x: int, y: int, z: int):
        # Position is relative to scanner that found this beacon
        self.x = x
        self.y = y
        self.z = z
        self.neighbor_distance = []

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        """
        Equality of absolute beacons
        """
        return self.x == other.x and self.y == other.y and self.z == other.z

    def add_neighbor(self, beacon):
        """
        Add a neighbor, FOUND BY THE SAME SCANNER

        :param beacon: Another beacon
        """
        # distance = (self.x - beacon.x) ** 2 + (self.y - beacon.y) ** 2 + (self.z - beacon.z) ** 2
        distance = [abs(self.x - beacon.x), abs(self.y - beacon.y), abs(self.z - beacon.z)]
        self.neighbor_distance.append(distance)

    def equal_beacons(self, other):
        """
        Two beacons are considered equal if they have 11 or more similar distances

        :param other: Another beacon
        :return: True if the two beacons have 11 or more similar distances, False otherwise
        """
        num_duplicates = 0
        for distance in self.neighbor_distance:
            for dist in other.neighbor_distance:
                if self.equal_distance(dist, distance):
                    num_duplicates += 1
        return num_duplicates > 10

    def absolute_position(self, scanner: 'Scanner') -> tuple:
        """

        :param scanner: Absolute scanner
        :return:
        """
        new_pos = transform_position((self.x, self.y, self.z), scanner.orientation[0], scanner.orientation[1])
        x = scanner.x + new_pos[0]
        y = scanner.y + new_pos[1]
        z = scanner.z + new_pos[2]
        return x, y, z

    @staticmethod
    def equal_distance(distance1: list, distance2: list) -> bool:
        for dist in distance1:
            if dist not in distance2:
                return False
        return True

    # def angle_position(self, axis, orientation):
    #     """
    #     Return the value of the given axis (axis 0 = x, axis 1 = y, axis 2 = z) considering the given angle
    #     """
    #     index = [abs(val) for val in angle].index(axis)
    #     if index == 0:
    #         return self.x if angle[index] >= 0 else -self.x
    #     if index == 1:
    #         return self.y if angle[index] >= 0 else -self.y
    #     if index == 2:
    #         return self.z if angle[index] >= 0 else -self.z


class Scanner:
    def __init__(self, number: int):
        self.num = number
        self.x = None
        self.y = None
        self.z = None
        self.orientation = None
        self.overlapping_scanners = {}
        self.beacons = []
        self.has_processed = False

    def __repr__(self):
        return f"<Scanner ({self.x}, {self.y}, {self.z}, {self.orientation}): {str(self.beacons)}>"

    def set_position(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def add_beacon(self, x: int, y: int, z: int) -> None:
        new_beacon = Beacon(x, y, z)
        for beacon in self.beacons:
            beacon.add_neighbor(new_beacon)
            new_beacon.add_neighbor(beacon)
        self.beacons.append(new_beacon)

    def determine_overlap(self, other: 'Scanner') -> bool:
        """
        Determine overlapping beacons by finding at least 12 common beacons in sensor range
        Find patterns in beacons of one scanner that match patterns in the other scanner
        Patterns can be found by looking that the distances between beacons
         if two beacons from each scanner have many similar distances, then they might be the same beacon

        :param other: Another scanner
        :return: True if there are at least 12 common beacons, False otherwise
        """
        num_beacons = 0
        stop = False
        for i, beacon1 in enumerate(self.beacons):
            # Time save, since this function takes the most time due to repeated looping
            if stop or i > len(self.beacons) - 15:
                break
            for beacon2 in other.beacons:
                if beacon1.equal_beacons(beacon2):
                    if other not in self.overlapping_scanners:
                        self.overlapping_scanners[other] = []
                        other.overlapping_scanners[self] = []
                    self.overlapping_scanners[other].append([beacon1, beacon2])
                    other.overlapping_scanners[self].append([beacon2, beacon1])
                    num_beacons += 1
                    if num_beacons == 2:
                        stop = True
                        break
        if num_beacons > 0:
            return True
        return False

    def determine_absolute_position(self, scanner: 'Scanner'):
        """
        Assign absolute x, y and z values to the scanner, based on another absolute scanner and a common beacon
        First, identify which way the scanner faces and its rotation
        Then, identify its location

        :param scanner: An absolute scanner
        """
        solution = None
        same_beacons = self.overlapping_scanners[scanner]
        orientations = all_orientations()
        for orientation in orientations:
            pair1 = 0
            pair2 = 1
            # First pair produces possible positions of the scanner
            unknown_beacon = same_beacons[pair1][0]
            known_beacon = same_beacons[pair1][1]
            loc = self.absolute_scanner_position(orientation, unknown_beacon, known_beacon, scanner)

            # Check 2nd pair to find position
            unknown_beacon = same_beacons[pair2][0]
            known_beacon = same_beacons[pair2][1]
            new_loc = self.absolute_scanner_position(orientation, unknown_beacon, known_beacon, scanner)
            if loc == new_loc:
                solution = (loc, orientation)
                break

        # print(f"Scanner {self.num} from scanner {scanner.num}: {solution}")
        angle = solution[1]
        coords = solution[0]
        self.orientation = angle
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]

    @staticmethod
    def absolute_scanner_position(orientation: tuple, beacon: Beacon, known_beacon: Beacon, known_scanner: 'Scanner'):
        """
        Compute the position of a beacon, based on a given beacon and angle
        Known beacon is relative to a beacon with known position and rotation

        :param orientation: The orientation used to orient the unknown beacon
        :param beacon: The beacon used to determine the expected location of the unknown scanner
        :param known_beacon: The corresponding beacon from a known scanner
        :param known_scanner: The known scanner associated with the known beacon
        :return:
        """
        oriented_beacon = transform_position((beacon.x, beacon.y, beacon.z), orientation[0], orientation[1])
        x = known_beacon.absolute_position(known_scanner)[0] - oriented_beacon[0]
        y = known_beacon.absolute_position(known_scanner)[1] - oriented_beacon[1]
        z = known_beacon.absolute_position(known_scanner)[2] - oriented_beacon[2]
        return [x, y, z]


class Task19(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 19

    def preprocess(self, data: list) -> list:
        output = []
        scanner = []
        i = 0
        for element in data:
            if len(element) == 4:
                scanner = Scanner(i)
                i += 1
            elif element == "":
                output.append(scanner)
            else:
                x, y, z = element.split(',')
                scanner.add_beacon(int(x), int(y), int(z))
        output.append(scanner)
        output[0].set_position(0, 0, 0)
        output[0].orientation = (0, 0)
        return output

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        # Find which scanners overlap
        for i, scanner1 in enumerate(data):
            for j, scanner2 in enumerate(data):
                if i >= j:
                    continue
                scanner1.determine_overlap(scanner2)

        # Convert all scanners and beacons to absolute
        absolute_beacons = []
        scanners_to_do = [data[0]]
        data[0].has_processed = True
        while len(scanners_to_do) != 0:
            scanner = scanners_to_do.pop()

            # Add beacons of scanner to list of absolute beacons
            for beacon in scanner.beacons:
                x, y, z = beacon.absolute_position(scanner)
                absolute = Beacon(x, y, z)
                # print(f"Absolute beacon: {absolute}")
                if absolute not in absolute_beacons:
                    absolute_beacons.append(absolute)

            # Find absolute position of overlapping scanners and add in queue
            for scan in scanner.overlapping_scanners:
                if scan.has_processed is False:
                    scan.has_processed = True
                    scan.determine_absolute_position(scanner)
                    scanners_to_do.append(scan)
        return len(absolute_beacons)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        # Find which scanners overlap
        for i, scanner1 in enumerate(data):
            for j, scanner2 in enumerate(data):
                if i >= j:
                    continue
                scanner1.determine_overlap(scanner2)

        # Convert all scanners and beacons to absolute
        scanners_to_do = [data[0]]
        data[0].has_processed = True
        while len(scanners_to_do) != 0:
            scanner = scanners_to_do.pop()
            # Find absolute position of overlapping scanners and add in queue
            for scan in scanner.overlapping_scanners:
                if scan.has_processed is False:
                    scan.has_processed = True
                    scan.determine_absolute_position(scanner)
                    scanners_to_do.append(scan)

        # Find largest manhattan distance between scanners
        max_distance = 0
        for scanner1 in data:
            for scanner2 in data:
                distance = self.manhattan_distance(scanner1, scanner2)
                if distance > max_distance:
                    max_distance = distance
        return max_distance

    @staticmethod
    def manhattan_distance(scanner1: Scanner, scanner2: Scanner) -> int:
        return abs(scanner1.x - scanner2.x) + abs(scanner1.y - scanner2.y) + abs(scanner1.z - scanner2.z)


if __name__ == "__main__":
    # Load task
    t = Task19()

    # Run task
    t.run_all()
