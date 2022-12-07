from utils.decorators import timer, debug
from utils.task import Task


class Task7(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 7

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        nums = self.get_directory_sizes(data)
        return sum([num for num in nums if num < 100000])

    def get_directory_sizes(self, data):
        structure = {"/": ([0], {})}
        cwd = []
        for line in data:
            # Command
            if line[1] == "ls":
                continue
            if line[0] == "$":
                if line[2] == "..":
                    cwd.pop(-1)
                else:
                    cwd.append(line[2])
            # directory info
            else:
                # New directory
                if line[0] == "dir":
                    folder = structure
                    for directory in cwd:
                        folder = folder[directory][1]
                    folder[line[1]] = ([0], {})
                # New file
                else:
                    folder = structure
                    for directory in cwd:
                        folder[directory][0][0] += int(line[0])
                        folder = folder[directory][1]
                    # Not needed to actually add the files to the structure
                    # folder[line[1]] = int(line[0])
        nums = self.find_numbers(structure)
        return nums

    def find_numbers(self, structure: dict) -> list:
        nums = []
        for key in structure.keys():
            nums.append(structure[key][0][0])
            nums.extend(self.find_numbers(structure[key][1]))
        return nums

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        space = self.get_directory_sizes(data)
        required_space = 30000000 - (70000000 - space[0])
        space.sort()
        for dir_space in space:
            if dir_space > required_space:
                return dir_space


if __name__ == "__main__":
    # Load task
    t = Task7()

    # Run task
    t.run_all()
