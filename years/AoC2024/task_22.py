from functools import cache
from utils.decorators import timer, debug_shape
from utils.task import Task


class Task22(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 22

    def preprocess(self, data: list) -> list:
        return [bin(int(num))[2:] for num in data]

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        total = 0
        for num in data:
            for i in range(2000):
                num = self.produce_secret_numbers(num)
            total += int(num, 2)
        return total

    @staticmethod
    def muliply(num: bin, bits: int) -> bin:
        return num + "0" * bits

    @staticmethod
    def divide(num: bin, bits: int = 5) -> bin:
        return num[:-bits]

    @staticmethod
    def mix(num1: bin, num2: bin) -> bin:
        tnum1 = "0" * max(0, len(num2) - len(num1)) + num1
        tnum2 = "0" * max(0, len(num1) - len(num2)) + num2
        return "".join(['1' if left != right else '0' for left, right in zip(tnum1, tnum2)])

    @staticmethod
    def prune(num: bin) -> bin:
        return num[len(num) - 24:] if len(num) > 24 else num

    @cache
    def produce_secret_numbers(self, num: bin) -> bin:
        num = self.prune(self.mix(num, self.muliply(num, 6)))
        num = self.prune(self.mix(self.divide(num), num))
        num = self.prune(self.mix(num, self.muliply(num, 11)))
        return num

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        founds = {}
        for num in data:
            found_sequences = {}
            prev_bananas = 111
            prev_sequence = [-111, -111, -111, -111]
            for i in range(2000):
                num = self.produce_secret_numbers(num)
                diff = int(str(int(num, 2))[-1]) - prev_bananas
                prev_bananas = int(str(int(num, 2))[-1])
                prev_sequence.pop(0)
                prev_sequence.append(diff)
                hash_sequence = ",".join([str(diff) for diff in prev_sequence])
                if hash_sequence not in found_sequences:
                    found_sequences[hash_sequence] = int(str(int(num, 2))[-1])
            for sequence in found_sequences:
                if sequence not in founds:
                    founds[sequence] = []
                founds[sequence].append(found_sequences[sequence])
        most_bananas = 0
        for values in founds.values():
            if sum(values) > most_bananas:
                most_bananas = sum(values)
        return most_bananas


if __name__ == "__main__":
    # Load task
    t = Task22()

    # Run task
    t.run_all()
