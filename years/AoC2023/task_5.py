from utils.decorators import timer, debug
from utils.task import Task


class Task5(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 5

    def preprocess(self, data: list) -> tuple:
        mappings = []
        current_mapping = []
        for line in data[3:]:
            if line == "":
                continue
            if not line[0].isnumeric():
                mappings.append(current_mapping)
                current_mapping = []
                continue
            # Create mapping range
            current_mapping.append([int(line[1]), int(line[2]), int(line[0])])
        mappings.append(current_mapping)
        return [int(num) for num in data[0][1:]], mappings

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: tuple) -> int:
        minimal_location = 999999999999
        seeds, almanac = data
        for seed in seeds:
            location = self.process_seed(almanac, seed)
            minimal_location = location if location < minimal_location else minimal_location
        return minimal_location

    @staticmethod
    def process_seed(almanac, seed):
        # Process seed
        for table in almanac:
            # Convert source id to destination id based on table
            for mapping in table:
                if mapping[0] <= seed <= mapping[0] + mapping[1]:
                    seed = mapping[2] - mapping[0] + seed
                    break
        return seed

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: tuple) -> int:
        seeds, almanac = data
        ranges = [range(seed, seed + seeds[i + 1]) for i, seed in enumerate(seeds) if i % 2 == 0]
        location = 0
        while True:
            seed = location
            for table in almanac[::-1]:
                for mapping in table:
                    if mapping[2] <= seed <= mapping[2] + mapping[1]:
                        seed = mapping[0] - mapping[2] + seed
                        break
            for r in ranges:
                if seed in r:
                    return location
            location += 1


if __name__ == "__main__":
    # Load task
    t = Task5()

    # Run task
    t.run_all()
