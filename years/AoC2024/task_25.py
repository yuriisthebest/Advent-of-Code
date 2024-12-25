from utils.decorators import timer, debug
from utils.task import Task


class Task25(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 25

    def preprocess(self, data: list) -> tuple:
        locks = []
        keys = []
        for i, line in enumerate(data):
            if line == "":
                if data[i+1][0] == "#":
                    locks.append(self.extract_lock(data[i+1:i+8]))
                else:
                    keys.append(self.extract_key(data[i+1:i+8]))
        return locks, keys

    @staticmethod
    def extract_lock(lock: list) -> list:
        representation = [None, None, None, None, None]
        for j, row in enumerate(lock):
            for k, val in enumerate(row):
                if val == "." and representation[k] is None:
                    representation[k] = j - 1
        return representation

    @staticmethod
    def extract_key(key: list) -> list:
        representation = [None, None, None, None, None]
        for j, row in enumerate(key):
            for k, val in enumerate(row):
                if val == ".":
                    representation[k] = 5 - j
        return representation

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        total_fits = 0
        locks, keys = data
        for lock in locks:
            for key in keys:
                total_fits += 1 if not self.has_overlap(lock, key) else 0
        return total_fits

    @staticmethod
    def has_overlap(lock: list, key: list):
        for lock_val, key_val in zip(lock, key):
            if lock_val + key_val > 5:
                return True
        return False

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """No second challenge for the last day"""
        return 0


if __name__ == "__main__":
    # Load task
    t = Task25()

    # Run task
    t.run_all()
