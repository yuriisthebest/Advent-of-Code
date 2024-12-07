from utils.decorators import timer, debug
from utils.task import Task


class Task7(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 7

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        calibration_result = 0
        for line in data:
            subtotal = int(line[0][:-1])
            values = [int(num) for num in line[1:]]
            if self.can_evaluated(subtotal, values, False):
                calibration_result += subtotal
        return calibration_result

    def can_evaluated(self, total: int, values: list, part2: bool) -> bool:
        if len(values) == 1:
            return values[0] == total
        return (self.can_evaluated(total, [values[0] + values[1], *values[2:]], part2)
                or self.can_evaluated(total, [values[0] * values[1], *values[2:]], part2)
                or (part2
                    and self.can_evaluated(total, [int(str(values[0]) + str(values[1])), *values[2:]], part2)))

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        calibration_result = 0
        for line in data:
            subtotal = int(line[0][:-1])
            values = [int(num) for num in line[1:]]
            if self.can_evaluated(subtotal, values, True):
                calibration_result += subtotal
        return calibration_result


if __name__ == "__main__":
    # Load task
    t = Task7()

    # Run task
    t.run_all()
