from utils.decorators import timer, debug
from utils.task import Task


class Task5(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 5

    def preprocess(self, data: list) -> tuple:
        index = data.index('')
        stacks = {int(i): [] for i in data[index-1] if i != ''}
        for line in data[:index-1]:
            crates = line.split('|')
            for i, crate in enumerate(crates):
                if crate == '':
                    continue
                crate = crate[1:2]
                stacks[i+1].append(crate)
        moves = []
        for move in data[index+1:]:
            moves.append([int(move[1]), int(move[3]), int(move[5])])
        return stacks, moves

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> str:
        stacks, moves = data
        for move in moves:
            count, source, target = move
            for _ in range(count):
                crate = stacks[source].pop(0)
                stacks[target].insert(0, crate)
        return "".join([stacks[column][0] for column in stacks])

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> str:
        stacks, moves = data
        for move in moves:
            count, source, target = move
            crane_hold = []
            for _ in range(count):
                crate = stacks[source].pop(0)
                crane_hold.insert(0, crate)
            for crate in crane_hold:
                stacks[target].insert(0, crate)
        return "".join([stacks[column][0] for column in stacks])


if __name__ == "__main__":
    # Load task
    t = Task5()

    # Run task
    t.run_all()
