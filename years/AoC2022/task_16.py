from utils.decorators import timer, debug
from utils.task import Task
import string
import copy
import itertools


class Valve:
    def __init__(self, name: str, pressure: int, tunnels: list):
        self.name = name
        self.pressure = pressure
        self.tunnels = [tunnel.translate(str.maketrans('', '', string.punctuation)) for tunnel in tunnels]
        self.distances = {0: [self.name]}
        self.paths = {}

    def __repr__(self):
        return f"{self.name}{self.pressure}"


class Task16(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 16

    def preprocess(self, data: list) -> dict:
        return {valve[1]: Valve(valve[1], int(valve[4][5:-1]), valve[9:]) for valve in data}

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: dict) -> int:
        data = self.setup_valves(data)
        start_position = "AA"
        score, sequence = self.find_optimal_sequence(data, start_position, 30)
        return score

    @staticmethod
    def setup_valves(data: dict):
        """
        Find and store for each valve, the distance it takes to go to any other valve

        :param data: Dictionary with all valves in the cave
        :return: Dictionary with all valves in the cave and the distances between each valve
        """
        # Calculate all paths from each vale to each other
        for valve in data.values():
            seen = [valve.name]
            i = 0
            while len(seen) < len(data):
                neighbors = valve.distances[i]
                valve.distances[i + 1] = []
                for known_neighbor in neighbors:
                    next_neighbors = data[known_neighbor].tunnels
                    for neighbor in next_neighbors:
                        if neighbor in seen:
                            continue
                        seen.append(neighbor)
                        valve.distances[i + 1].append(neighbor)
                i += 1
            # Reverse distances dict
            for distance in valve.distances:
                for node in valve.distances[distance]:
                    valve.paths[node] = distance
        return data

    def find_optimal_sequence(self, valves: dict, start_position: str, max_time: int):
        """
        Check all possible sequences of opening valves to find the sequence that releases the most pressure

        :param valves: All valves, so the distance between valves can be found
        :param start_position: The starting position of the sequence (always 'AA')
        :param max_time: The amount of time before the simulation stops
        :return: The maximum amount of pressure released in the timeframe and the sequence that releases it
        """
        # Find all sequences of opening values
        possible_sequences = self.all_possible_sequences(valves, start_position, max_time)
        # Determine to optimal sequence
        max_score = 0
        max_seq = None
        for sequence in possible_sequences:
            new_score = self.calculate_score(sequence, valves, start_position, max_time)
            if new_score > max_score:
                max_score = new_score
                max_seq = sequence
        return max_score, max_seq

    @staticmethod
    def all_possible_sequences(valves: dict, start_position: str, max_time: int):
        """
        Generate all sequences of opening valves that fit within the given timeframe

        :param valves: All valves, so the distance between valves can be found
        :param start_position: The starting position of the sequence (always 'AA')
        :param max_time: The amount of time before the simulation stops
        :return: Finite generator
        """
        possible_valves = [valve for valve in valves.values() if valve.pressure != 0]
        max_length = len(possible_valves)
        todo = [([valve], valves[start_position].paths[valve.name] + 1)
                for valve in valves.values() if valve.pressure != 0]
        new_todo = []
        while len(todo) != 0:
            # Take a subsequence and try to add more valves to the end
            current_sequence, sequence_time = todo.pop()
            if len(current_sequence) == max_length:
                yield current_sequence
            # Keep adding new valves if they can be opened within the timelimit
            for valve in possible_valves:
                if valve in current_sequence:
                    continue
                time_taken = valves[current_sequence[-1].name].paths[valve.name] + 1
                if time_taken + sequence_time < max_time:
                    new_todo.append((current_sequence + [valve], sequence_time + time_taken))
                else:
                    # The current sequence can't be appended by this specific valve, so release sequence as optimal
                    # I now realise that this causes some duplicates to be released
                    yield current_sequence
            # Refresh the list of sequences to try and append
            if len(todo) == 0:
                todo = new_todo
                new_todo = []

    @staticmethod
    def calculate_score(sequence: list, valves: dict, start_position: str, max_time: int) -> int:
        """
        Given a sequence of valves to open, calculate the amount of pressure that is released in the given timeframe

        :param sequence: The sequence of valves that is opened in the quickest time possible
        :param valves: All valves, so the distance between valves can be found
        :param start_position: The starting position of the sequence (always 'AA')
        :param max_time: The amount of time before the simulation stops
        :return: The total amount of pressure released
        """
        time = 0
        score = 0
        time_score = 0
        position = start_position
        for valve in sequence:
            # Got to value and open it
            time_spent = valves[position].paths[valve.name] + 1
            if time_spent + time > max_time:
                score += (max_time - time) * time_score
                return score
            time += time_spent
            position = valve.name
            # Score achieved while opening next valve
            score += time_spent * time_score
            # New time score
            time_score += valve.pressure
        # Score for the remaining time
        score += (max_time - time) * time_score
        return score

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: dict) -> int:
        data = self.setup_valves(data)
        partitions = self.partition(data)
        start_position = "AA"
        best_score = 0
        for p1, p2 in partitions:
            # Setup partitions
            partition1 = copy.deepcopy(data)
            partition2 = copy.deepcopy(data)
            for valve in partition1:
                if valve in p1:
                    partition1[valve].pressure = 0
            for valve in partition2:
                if valve in p2:
                    partition2[valve].pressure = 0
            # Find the score for the human and elephant
            score1, sequence1 = self.find_optimal_sequence(partition1, start_position, 26)
            score2, sequence2 = self.find_optimal_sequence(partition2, start_position, 26)
            if score1 + score2 > best_score:
                best_score = score1 + score2
                # Solution: [PH11, AW21, LX22, IN16, OW25, BE5, PB4], [HX14, QR20, SV24, HH12, FY17, RM18]
        return best_score

    @staticmethod
    def partition(valves: dict):
        """
        Partition the input into two sets containing all pressurized valves
        The partition is symmetric, so partition A is always equal or larger than partition B

        :param valves: A dictionary with all valves in the cave
        :return: Finite generator
        """
        pressured_valves = set([valve.name for valve in valves.values() if valve.pressure != 0])
        for i in range(len(pressured_valves) // 2 + 1):
            combinations = itertools.combinations(pressured_valves, i)
            for comb in combinations:
                yield comb, pressured_valves.difference(comb)


if __name__ == "__main__":
    # Load task
    t = Task16()

    # Run task
    t.run_all()
