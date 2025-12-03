from utils.decorators import timer, debug_shape
from utils.task import Task


class Task3(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 3

    def preprocess(self, data: list) -> list:
        return [[int(num) for num in line] for line in data]

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        result = 0
        for bank in data:
            # find max
            first_value = max(bank[:-1])
            index = bank.index(first_value)
            second_value = max(bank[index+1:])
            result += int(str(first_value) + str(second_value))
        return result

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        result = 0
        for bank in data:
            start_index = 0
            largest_values = []
            for i in range(12)[::-1]:
                # Find appropiate value
                window = bank[start_index:-i] if i > 0 else bank[start_index:]
                value = max(window)
                largest_values.append(value)
                # Change the start index to the found value
                index = window.index(value)
                start_index += index + 1
            # Calculate jolts
            result += int("".join([str(val) for val in largest_values]))
        return result


if __name__ == "__main__":
    # Load task
    t = Task3()

    # Run task
    t.run_all()
