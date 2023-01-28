from utils.decorators import timer, debug
from utils.task import Task
import tqdm
import re

ROCK_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 1), (1, 1), (1, 2), (1, 0), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
]


class Rock:
    def __init__(self, shape, height: int):
        self.shape = shape
        self.position = (2, height)

    def move_rock(self, cave, jet) -> bool:
        # First, move the rock according to jetstream
        x = 1 if jet == ">" else -1
        new_position = (self.position[0] + x, self.position[1])
        if not self.check_collision(cave, new_position):
            self.position = new_position
        # Now, move the rock down, if possible
        new_position = (self.position[0], self.position[1] - 1)
        if not self.check_collision(cave, new_position):
            self.position = new_position
            return False
        # The rock has come to a stop
        return True

    def check_collision(self, cave, new_position) -> bool:
        for delta_position in self.shape:
            # If new position is too far left or below cave, it collides
            if new_position[0] + delta_position[0] < 0 or new_position[1] + delta_position[1] < 0:
                return True
            # If new position is too far right, it collides
            if new_position[0] + delta_position[0] >= 7:
                return True
            # If new position is on a blocked space, it collides
            if (new_position[1] + delta_position[1] in cave
                    and new_position[0] + delta_position[0] in cave[new_position[1] + delta_position[1]]):
                return True
        # If no position of rock is blocked, it does not collide
        return False


class Task17(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 17

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        # Cave {HEIGHT: [blocked rocks]}
        cave = {0: []}
        jet_index = 0
        for i in range(2022):
            height = max(cave) + 4 if not i == 0 else 3
            rock = Rock(shape=ROCK_SHAPES[i % len(ROCK_SHAPES)], height=height)
            jet_index = self.simulate_rock(cave, rock, data[0], jet_index)
        return max(cave) + 1

    @staticmethod
    def simulate_rock(cave, rock, jets, jet_start) -> int:
        stopped = False
        while not stopped:
            stopped = rock.move_rock(cave, jets[jet_start])
            jet_start += 1
            jet_start %= len(jets)
        for delta_position in rock.shape:
            true_position = (rock.position[0] + delta_position[0], rock.position[1] + delta_position[1])
            if true_position[1] not in cave:
                cave[true_position[1]] = []
            cave[true_position[1]].append(true_position[0])
        return jet_start

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        iterations = 1000000000000
        # Cave {HEIGHT: [blocked rocks]}
        cave = {0: []}
        jet_index = 0
        pattern_period = None
        pattern_start = None
        for i in tqdm.trange(iterations):
            # Stop simulating when cycles are known
            if pattern_start is not None and i % pattern_period == pattern_start + left_over_simulations:
                break
            # Simulate rocks until cycles are known
            height = max(cave) + 4 if not i == 0 else 3
            rock = Rock(shape=ROCK_SHAPES[i % len(ROCK_SHAPES)], height=height)
            jet_index = self.simulate_rock(cave, rock, data[0], jet_index)
            if i == 8000:
                pattern = self.find_cycles(cave)
                if pattern is not None:
                    pattern_period = int(pattern[0])
                    pattern_start = int(pattern[1]) + 1
                    left_over_simulations = (iterations - pattern_start) % pattern_period
                    cycle_height = int(pattern[0])
        num_cycles = (iterations - 8000 - pattern_start) // pattern_period
        return max(cave) + 1 + (cycle_height * num_cycles)
    # 1580813953441 (too low)

    @staticmethod
    def find_cycles(cave):
        cave_binary = " ".join(["".join([f"1" if num in cave[i] else f"0" for num in range(7)]) for i in cave])
        p = re.compile(r'(.+?)\1+')
        pattern = [pattern for pattern in re.findall(p, cave_binary) if len(pattern) > 100]
        div_num = 8
        for pat in pattern:
            indexes = [(m.start(0), m.end(0)) for m in re.finditer(pat, cave_binary)]
            # print(len(pat), len(pat) / div_num, indexes[0][0] / div_num, indexes)
            # print(cave_binary[indexes[0][0]:indexes[0][0] + div_num])
            if len(pat) % div_num == 0 and indexes[0][0] % div_num == div_num-1:
                return len(pat) / div_num, indexes[0][0] / div_num
        return 0, 0


if __name__ == "__main__":
    # Load task
    t = Task17()

    # Run task
    t.run_all()
