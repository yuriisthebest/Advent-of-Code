from utils.decorators import timer, debug
from utils.task import Task


class Task2(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 2

    def preprocess(self, data: list) -> list:
        return [[int(num) for num in line] for line in data]

    def is_safe_dampened(self, report: list, ascending: bool, safeties: int = 1) -> bool:
        i = 0
        while i < len(report) - 1:
            if i >= len(report) - 1:
                continue
            num = report[i]
            next_num = report[i + 1]
            if ascending and (num >= next_num or num < next_num - 3):
                if safeties > 0:
                    return self.recurse_without_bad_level(ascending, i, report, safeties)
                else:
                    return False
            if not ascending and (num <= next_num or num > next_num + 3):
                if safeties > 0:
                    return self.recurse_without_bad_level(ascending, i, report, safeties)
                else:
                    return False
            i += 1
        return True

    def recurse_without_bad_level(self, ascending, i, report, safeties):
        safeties -= 1
        new_1 = report.copy()
        new_2 = report.copy()
        del new_1[i]
        del new_2[i + 1]
        return (self.is_safe_dampened(new_1, ascending, safeties)
                or self.is_safe_dampened(new_2, ascending, safeties))

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        num_safe = 0
        for report in data:
            if self.is_safe_dampened(report, True, 0) or self.is_safe_dampened(report, False, 0):
                num_safe += 1
        return num_safe

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        num_safe = 0
        for report in data:
            if self.is_safe_dampened(report, True, 1) or self.is_safe_dampened(report, False, 1):
                num_safe += 1
        return num_safe


if __name__ == "__main__":
    # Load task
    t = Task2()

    # Run task
    t.run_all()
