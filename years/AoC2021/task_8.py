from utils.decorators import timer, debug
from utils.task import Task

# Task constants
LENGTHS = {0: 6,  # 0, 6, 9
           1: 2,  # Unique
           2: 5,  # 2, 3, 5
           3: 5,  # 2, 3, 5
           4: 4,  # Unique
           5: 5,  # 2, 3, 5
           6: 6,  # 0, 6, 9
           7: 3,  # Unique
           8: 7,  # Unique
           9: 6}  # 0, 6, 9
UNIQUES = {2: 1, 3: 7, 4: 4, 7: 8}


def all_in(word: str, match: str) -> bool:
    """
    Return true if all letters in match are in the word
    """
    for letter in match:
        if letter not in word:
            return False
    return True


class Task8(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 8

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        count = 0
        for entry in data:
            values = entry[-4:]
            for val in values:
                if len(val) in [2, 3, 4, 7]:
                    count += 1
        return count

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        count = 0
        sig4, sig7, sig8 = None, None, None
        for entry in data:
            configuration = {}
            signals = entry[:10]
            # Find and remember the signals for the numbers 1, 7, 4 and 8
            for signal in signals:
                if len(signal) == 2:
                    configuration["right"] = signal
                if len(signal) == 3:
                    sig7 = signal
                if len(signal) == 4:
                    sig4 = signal
                if len(signal) == 7:
                    sig8 = signal
            # Find the signal values for the bottom and bottom-left segments
            configuration["left-under"] = ""
            for letter in sig8:
                if letter not in sig4 and letter not in sig7:
                    configuration["left-under"] += letter

            code = []
            values = entry[-4:]
            for val in values:
                # Add 1, 4, 7, 8 to code
                if len(val) in [2, 3, 4, 7]:
                    code.append(str(UNIQUES[len(val)]))
                    continue
                # Add 2, 3, 5 to code
                if len(val) == 5:
                    if all_in(val, configuration['right']):
                        code.append("3")
                    elif all_in(val, configuration['left-under']):
                        code.append("2")
                    else:
                        code.append("5")
                    continue
                # Add 0, 6, 9 to code
                if len(val) == 6:
                    if not all_in(val, configuration['left-under']):
                        code.append("9")
                    elif all_in(val, configuration['right']):
                        code.append("0")
                    else:
                        code.append("6")
            count += int("".join(code))
        return count


if __name__ == "__main__":
    # Load task
    t = Task8()

    # Run task
    t.run_all()
