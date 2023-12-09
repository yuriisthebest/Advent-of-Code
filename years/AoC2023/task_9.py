from utils.decorators import timer, debug
from utils.task import Task


class Task9(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 9

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        total = 0
        for line in data:
            line = [int(value) for value in line]
            differences = self.extrapolate_history(line)
            total += self.predict_next(differences)
        return total

    def extrapolate_history(self, history: list) -> list:
        full_history = []
        while any(value != 0 for value in history):
            full_history.append(history)
            history = self.find_differences(history)
        return full_history

    @staticmethod
    def find_differences(line: list) -> list:
        differences = []
        for i, value in enumerate(line):
            if i == len(line) - 1:
                continue
            differences.append(line[i+1] - value)
        return differences

    @staticmethod
    def predict_next(differences: list) -> int:
        return sum([line[-1] for line in differences])

    @staticmethod
    def predict_previous(differences: list) -> int:
        result = 0
        for i, line in enumerate(differences[::-1]):
            result = line[0] - result
        return result

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        total = 0
        for line in data:
            line = [int(value) for value in line]
            differences = self.extrapolate_history(line)
            total += self.predict_previous(differences)
        return total


if __name__ == "__main__":
    # Load task
    t = Task9()

    # Run task
    t.run_all()
