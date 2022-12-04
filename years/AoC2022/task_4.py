from utils.decorators import timer, debug
from utils.task import Task


class Task4(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 4

    def preprocess(self, data: list) -> list:
        for i, pair in enumerate(data):
            elf1, elf2 = pair.split(',')
            data[i] = [range(*[int(x) for x in elf1.split('-')]),
                       range(*[int(x) for x in elf2.split('-')])]
        return data

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        contained_pairs = 0
        for pair in data:
            if pair[0].start <= pair[1].start and pair[0].stop >= pair[1].stop:
                contained_pairs += 1
                continue
            if pair[1].start <= pair[0].start and pair[1].stop >= pair[0].stop:
                contained_pairs += 1
        return contained_pairs

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        contained_pairs = 0
        for pair in data:
            if pair[0].start <= pair[1].start <= pair[0].stop:
                contained_pairs += 1
                continue
            if pair[1].start <= pair[0].start <= pair[1].stop:
                contained_pairs += 1
                continue
        return contained_pairs


if __name__ == "__main__":
    # Load task
    t = Task4()

    # Run task
    t.run_all()
