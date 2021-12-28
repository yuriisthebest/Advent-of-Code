from utils.decorators import timer, debug
from utils.task import Task


class Task3(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 3

    @staticmethod
    def find_common(data: list):
        counts = [0 for _ in data[0]]
        for value in data:
            for i, digit in enumerate(value):
                if digit == '1':
                    counts[i] += 1
        most = "0b"
        least = "0b"
        for count in counts:
            if count >= len(data) / 2:
                most += "1"
                least += "0"
            else:
                least += "1"
                most += "0"
        return int(most, 2) * int(least, 2), most, least

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        return self.find_common(data)[0]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        oxygen = data.copy()
        co2 = data.copy()
        final_ox, final_co2 = None, None
        for i in range(len(data[0])):
            oxygen, final_ox = self.check_numbers(oxygen, "most", i)
            co2, final_co2 = self.check_numbers(co2, "least", i)
            if final_ox is not None and final_co2 is not None:
                break
        final_ox = int("".join(final_ox), 2)
        final_co2 = int("".join(final_co2), 2)
        return final_ox * final_co2

    def check_numbers(self, data, binary, i):
        _, most, least = self.find_common(data)
        if binary == "most":
            b = most
        else:
            b = least
        temp_data = data.copy()
        for value in temp_data:
            if len(data) == 1:
                return data, data[0]
            digit = value[i]
            # If the digit is the most common digit, then it is not part of co2
            if digit != b[i + 2]:
                try:
                    data.remove(value)
                except ValueError:
                    pass
        return data, None


if __name__ == "__main__":
    # Load task
    t = Task3()

    # Run task
    t.run_all()
