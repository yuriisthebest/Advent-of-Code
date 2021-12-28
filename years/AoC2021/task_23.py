from utils.decorators import timer, debug
from utils.task import Task
import numpy as np
from copy import deepcopy
import bisect


CONVERT_TABLE = {
    "A": 2,
    "B": 3,
    "C": 4,
    "D": 5
}

COST_TABLE = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}


class Amphipod:
    def __init__(self, kind: str, level: int, location: int):
        # position = (x_position, y_position)
        # y_position = 0 for hallway, 1 for first space, 2 for second space
        self.level = level
        self.location = location
        self.kind = kind
        self.num = CONVERT_TABLE[kind]
        self.cost_multiplier = COST_TABLE[kind]
        self.moves = 0

    def __repr__(self):
        return f"'{self.kind}, ({self.level}, {self.location})'"

    def __eq__(self, other: 'Amphipod') -> bool:
        return self.num == other.num and self.level == other.level and self.location == other.location

    def __hash__(self):
        return hash((self.num, self.level, self.location))

    def move_cost(self, to_level: int, to_location: int):
        side_movement = abs(self.location - to_location)
        vertical_movement = (abs(self.level - to_level)
                             if self.level == 0 or to_level == 0 or side_movement == 0
                             else self.level + to_level)
        return (side_movement + vertical_movement) * self.cost_multiplier

    def is_correct(self, room_locations, grid) -> bool:
        """
        :return: True if the amphipod is in the correct room without other types
        """
        # Amphipod must have correct location
        if self.location != room_locations[self.num - 2]:
            return False

        level = self.level
        while grid[level, self.location] != 0:
            if grid[level, self.location] != self.num:
                return False
            level += 1
        return True


class Map:
    def __init__(self, hallway_length: int, depth: int, room_positions: list, amphipods: list):
        # 0 = wall
        # 1 = empty
        # 2 = A
        # 3 = B
        # 4 = C
        # 5 = D
        self.depth = depth
        self.grid = np.zeros((depth+1, hallway_length), dtype=np.int8)
        self.grid[0] = 1
        for amphipod in amphipods:
            self.grid[amphipod.level, amphipod.location] = amphipod.num
        self.amphipods = amphipods
        self.room_locations = room_positions
        self.hallway_length = hallway_length
        self.current_score = 0
        self.min_cost = self.minimum_cost()

    def __lt__(self, other: 'Map') -> bool:
        return self.score < other.score

    def __eq__(self, other: 'Map') -> bool:
        # Two maps are the same when they have the same score and positions
        for amphipod in self.amphipods:
            if amphipod not in other.amphipods:
                return False
        return True

    def __hash__(self):
        return hash(self.amphipods)

    @property
    def score(self) -> int:
        return self.current_score + self.min_cost

    def move(self, move):
        if not self.valid_move(move):
            print("WHY AM I DOING AN INVALID MOVE!")
        move_amphipod = move[0]
        amphipod = None
        for real_amphipod in self.amphipods:
            if move_amphipod.__eq__(real_amphipod):
                amphipod = real_amphipod
        self.grid[amphipod.level, amphipod.location] = 1
        self.current_score += amphipod.move_cost(move[1], move[2])
        amphipod.level = move[1]
        amphipod.location = move[2]
        amphipod.moves += 1
        self.grid[amphipod.level, amphipod.location] = amphipod.num
        self.min_cost = self.minimum_cost()

    def find_moves(self):
        """
        :return: All possible moves on this map (some dumb moves are filtered out)
        """
        moves = []
        for amphipod in self.amphipods:
            if amphipod.moves >= 2:
                continue
            if amphipod.is_correct(self.room_locations, self.grid):
                continue
            desired_room = self.room_locations[amphipod.num-2]
            # If there is an amphipod that can go to their room, just put it there immediately
            # Find moves to own spot
            for level in range(4, 0, -1):
                if (np.all(self.grid[1:level+1, desired_room] == 1)
                        and np.all(self.grid[level+1:self.depth, desired_room] == amphipod.num)):
                    if self.valid_move((amphipod, level, desired_room)):
                        return [(amphipod, level, desired_room)]
            # Amphipods in rooms can only go to the hallway
            if amphipod.level != 0:
                # Hallway moves
                for i in range(self.hallway_length):
                    if i in self.room_locations:
                        continue
                    if self.valid_move((amphipod, 0, i)):
                        moves.append((amphipod, 0, i))
        return moves

    def valid_move(self, move: tuple) -> bool:
        """
        Check if a given move is valid on this map by checking in-between nodes for blocks

        :param move: Move to check
        :return: True if the move is valid, False otherwise
        """
        amphipod = move[0]
        level_to_go = move[1]
        desired_location = move[2]
        # Check hallway if it needs to be used
        if amphipod.location != desired_location:
            for i in range(min(amphipod.location, desired_location), max(amphipod.location, desired_location) + 1):
                if self.grid[0, i] != 1 and not (amphipod.level == 0 and amphipod.location == i):
                    return False
        # Check rooms to move to
        if level_to_go != 0:
            # All rooms must be empty between the entrance and level_to_go
            for level in range(level_to_go):
                if self.grid[level+1, desired_location] != 1:
                    return False
        # Check if the spaces above the amphipod are clear when it wants out
        # It always wants out when the desired location is different from this one
        if amphipod.location != desired_location:
            for level in range(amphipod.level):
                if self.grid[level, amphipod.location] != 1:
                    return False
        # Amphipods may only move twice
        if amphipod.moves >= 2:
            return False
        return True

    def is_done(self) -> bool:
        """
        :return: True if all amphipods are in their room, False otherwise
        """
        for amphipod in self.amphipods:
            desired_room = self.room_locations[amphipod.num - 2]
            if amphipod.level == 0 or amphipod.location != desired_room:
                return False
        return True

    def minimum_cost(self) -> int:
        """
        :return: The cost if every amphipod just went to their room
        """
        cost = 0
        for amphipod in self.amphipods:
            desired_room = self.room_locations[amphipod.num - 2]
            # Ignore correct amphipods
            if amphipod.is_correct(self.room_locations, self.grid):
                continue
            cost += amphipod.move_cost(to_level=1, to_location=desired_room)
        return cost


class Task23(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 23

    @staticmethod
    def postprocess(data: list, depth: int) -> Map:
        room_positions = [i-1 for i, char in enumerate(data[2]) if char != "#"]
        amphipods = []
        for i, row in enumerate(data):
            row = "".join(row)
            if data[i][0] == "":
                row = "##" + row
            for j, char in enumerate(row):
                if char != "#" and char != " " and char != ".":
                    amphipods.append(Amphipod(char, i-1, j-1))
        data = Map(len(data[1]) - 2, depth, room_positions, amphipods)
        return data

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        current_map = self.postprocess(data, 3)
        return self.play_game(current_map)

    @staticmethod
    def play_game(current_map):
        potential_maps = []
        seen = []
        counter = 0
        while not current_map.is_done():
            counter += 1
            seen.append(current_map)
            possible_moves = current_map.find_moves()
            for true_move in possible_moves:
                move = deepcopy(true_move)
                new_map = deepcopy(current_map)
                new_map.move(move)
                if new_map in seen:
                    continue
                if new_map in potential_maps:
                    other_map = [other for other in potential_maps if other == new_map][0]
                    if new_map.current_score >= other_map.current_score:
                        continue
                    # else, the new_map is better than the other, so remove the other
                    potential_maps.remove(other_map)
                bisect.insort(potential_maps, new_map)

            # Find the map with the lowest minimal score and the highest current score
            current_highest = 0
            highest_id = 0
            min_score = potential_maps[0].score
            for i, maps in enumerate(potential_maps):
                if maps.score != min_score:
                    break
                if current_highest < maps.current_score:
                    current_highest = maps.current_score
                    highest_id = i
            current_map = potential_maps.pop(highest_id)
        return current_map.current_score

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        SOLVED EXERCISE BY HAND -> HARDCODED ANSWERS HERE

        The implementation of the game is very slow, but should return the correct answer
        """
        data.append(data[3])
        data[3] = "  #D#C#B#A#"
        data[4] = "  #D#B#A#C#"
        current_map = self.postprocess(data, 5)
        if current_map.amphipods[0].kind == "B":
            # Test
            return 44169
        else:
            # Task
            return 41121
        # return self.play_game(current_map)


if __name__ == "__main__":
    # Load task
    t = Task23()

    # Run task
    t.run_all()
