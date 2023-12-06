from utils.decorators import timer, debug
from utils.task import Task


class Task6(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 6

    def preprocess(self, data: list) -> list:
        time = []
        distance = []
        for element in data[0]:
            if element.isnumeric():
                time.append(int(element))
        for element in data[1]:
            if element.isnumeric():
                distance.append(int(element))
        return [[(a, b) for a, b in zip(time, distance)], data]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        result = 1
        for time, record in data[0]:
            result *= self.compute_number_of_options(time, record)
        return result

    @staticmethod
    def compute_number_of_options(time, record):
        charge_time = 0
        while (time - charge_time) * charge_time <= record:
            charge_time += 1
        minimal_charge_time = charge_time
        charge_time = time
        while (time - charge_time) * charge_time <= record:
            charge_time -= 1
        maximal_charge_time = charge_time
        num_options = maximal_charge_time - minimal_charge_time + 1
        return num_options

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        time = int("".join([elem for elem in data[1][0] if elem.isnumeric()]))
        record = int("".join([elem for elem in data[1][1] if elem.isnumeric()]))
        return self.compute_number_of_options(time, record)


if __name__ == "__main__":
    # Load task
    t = Task6()

    # Run task
    t.run_all()
