from utils.decorators import timer, debug
from utils.task import Task


class Elf:
    def __init__(self, row: int, column: int):
        self.x = column
        self.y = row

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def propose(self, directions: list, positions: dict) -> tuple:
        # If no-one nearby, do nothing
        found = False
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Skip itself
                if i == j == 0:
                    continue
                if self.x + i in positions and self.y + j in positions[self.x + i]:
                    found = True
                    break
        if not found:
            return -4000, -4000
        # Check, for each direction, if there is an elf in those tiles, if no, return that direction
        for direction in directions:
            found = False
            for relative_tile in direction:
                if (self.x + relative_tile[0] in positions
                        and self.y + relative_tile[1] in positions[self.x + relative_tile[0]]):
                    found = True
            if not found:
                # No elf has been found, so go that direction
                return self.x + direction[0][0], self.y + direction[0][1]
        return -4000, -4000

    def move(self, proposition: tuple) -> None:
        self.x = proposition[0]
        self.y = proposition[1]


class Task23(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 23

    def preprocess(self, data: list) -> list:
        return [Elf(i, j) for i, row in enumerate(data) for j, tile in enumerate(row) if tile == "#"]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        directions = self.initiate_directions()
        for _ in range(10):
            current_positions = self.position_hashtable(data)
            self.simulate_round(data, directions, current_positions)
        # Calculate score
        current_positions = [(elf.column, elf.row) for elf in data]
        min_x, max_x = min(current_positions)[0], max(current_positions)[0]
        min_y, max_y = min(current_positions, key=lambda x: x[1])[1], max(current_positions, key=lambda x: x[1])[1]
        return ((max_x - min_x + 1) * (max_y - min_y + 1)) - len(current_positions)

    @staticmethod
    def initiate_directions():
        # North=y-1, South=y+1, West=x-1, East=x+1
        north, west = -1, -1
        south, east = 1, 1
        directions = [[(0, north), (west, north), (east, north)],
                      [(0, south), (west, south), (east, south)],
                      [(west, 0), (west, north), (west, south)],
                      [(east, 0), (east, north), (east, south)]]
        return directions

    @staticmethod
    def simulate_round(data: list, directions: list, current_positions: dict) -> None:
        """
        Simulate a single round

        :param data: A list of all elves, which know their position
        :param directions: The list of directions to consider, in order
        :param current_positions: Quick hashmap to determine if there is an elf at a certain location
        """
        # Propose phase
        propositions = [(elf.propose(directions, current_positions), elf) for elf in data]
        propositions.sort(key=lambda x: x[0])
        # Act phase
        for i, proposition in enumerate(propositions):
            # Ignore -4000, -4000 propositions
            if proposition == (-4000, -4000):
                continue
            # Check for duplicate propositions
            if i >= 1 and propositions[i - 1][0] == proposition[0]:
                continue
            if i + 1 < len(propositions) and propositions[i + 1][0] == proposition[0]:
                continue
            # Move elf
            proposition[1].move(proposition[0])
        # Change directions
        direct = directions.pop(0)
        directions.append(direct)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        num_rounds = 0
        directions = self.initiate_directions()
        current_positions = self.position_hashtable(data)
        prev = {}
        while prev != current_positions:
            prev = current_positions
            self.simulate_round(data, directions, current_positions)
            # Setup next iteration
            current_positions = self.position_hashtable(data)
            num_rounds += 1
        return num_rounds

    @staticmethod
    def position_hashtable(data: list) -> dict:
        """
        Create a dictionary of the positions of the elves

        :param data: A list of all elves, which know their position
        :return: Hashmap to check if there is an elf at a certain location
        """
        current_positions = {}
        for elf in data:
            if elf.column not in current_positions:
                current_positions[elf.column] = {}
            current_positions[elf.column][elf.row] = True
        return current_positions


if __name__ == "__main__":
    # Load task
    t = Task23()

    # Run task
    t.run_all()
