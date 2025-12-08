from utils.decorators import timer, debug_shape
from utils.task import Task
from utils.data_structures.queue import PriorityQueue


class Distance:
    def __init__(self, box1: list, box2: list, distance_value: int):
        self.box1 = box1
        self.box2 = box2
        self.distance = distance_value

    def __lt__(self, other):
        return self.distance < other.distance

    def __repr__(self):
        return f"({self.distance}, {self.box1}, {self.box2})"

    def get(self, tag: str):
        return self.distance

    def boxes(self):
        return self.box1, self.box2


class Task8(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 8

    def preprocess(self, data: list) -> list:
        return [[int(num) for num in line.split(",")] for line in data]

    @staticmethod
    def distance(box1: list, box2: list):
        return (box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) ** 2 + (box1[2] - box2[2]) ** 2

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        distances = self.compute_and_sort_distance_matrix(data)
        seen = []
        circuits = []
        for i in range(10 if self.IS_TEST else 1000):
            self.add_connection(distances, seen, circuits)
        # Get the lengths of the circuits
        circuit_lengths = [len(circuit) for circuit in circuits]
        circuit_lengths.sort(reverse=True)
        return circuit_lengths[0] * circuit_lengths[1] * circuit_lengths[2]

    def compute_and_sort_distance_matrix(self, data):
        # Compute and sort distances between boxes
        distances = PriorityQueue("distance")
        for i, box1 in enumerate(data):
            for box2 in data[i:]:
                if box1 == box2:
                    continue
                dist = self.distance(box1, box2)
                sort_object = Distance(box1, box2, dist)
                distances.add(sort_object)
        return distances

    @staticmethod
    def add_connection(distances: PriorityQueue, seen: list, circuits: list):
        """
        Adds a single connection between boxes to the circuits

        :param distances: PriorityQueue containing a sorted list of distances between boxes
        :param seen: All the boxes that have already been processed at least once
        :param circuits: The current circuits made by previous connections
        :return: Two boxes which were considered in this add connection step
        """
        # Attempt to use the current shortest available boxes to make a new connection
        sortest_distance = distances.take_first()
        box1, box2 = sortest_distance.boxes()
        # Both boxes are not part of any circuit, add a new one for them
        if box1 not in seen and box2 not in seen:
            circuits.append([box1, box2])
            seen.extend([box1, box2])
        else:
            # Add boxes to be seen
            if box1 not in seen:
                seen.append(box1)
            if box2 not in seen:
                seen.append(box2)
            # Find which circuits these boxes might already be part of
            circuit1 = [c for c in circuits if box1 in c]
            circuit2 = [c for c in circuits if box2 in c]
            # If both boxes are in the same circuit, do nothing
            if circuit1 == circuit2:
                return box1, box2
            # Add a new box to an existing circuit
            if len(circuit1) == 0:
                circuit2[0].append(box1)
            elif len(circuit2) == 0:
                circuit1[0].append(box2)
            # Combine the two different circuits
            else:
                circuit1[0].extend(circuit2[0])
                circuits.remove(circuit2[0])
        return box1, box2

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        distances = self.compute_and_sort_distance_matrix(data)
        seen = []
        circuits = []
        box1, box2 = None, None
        while len(circuits) == 0 or len(circuits[0]) < len(data):
            box1, box2 = self.add_connection(distances, seen, circuits)
        # Return the X-coords of the boxes that made the final connection
        return box1[0] * box2[0]


if __name__ == "__main__":
    # Load task
    t = Task8()

    # Run task
    t.run_all()
