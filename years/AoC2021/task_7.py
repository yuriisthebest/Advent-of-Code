from utils.decorators import timer, debug
from utils.task import Task
from utils.load import load_task_json


def calculate_fuel(data: list, position: int) -> int:
    return sum([abs(position - num) for num in data])


def calculate_fuel_part_2(data: list, position: int) -> int:
    return sum([sum([value+1 for value in range(abs(position - num))]) for num in data])


class Task7(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 7

    def load(self) -> tuple:
        test, task = load_task_json(self.YEAR, self.TASK_NUM)
        test = self.preprocess(test)
        task = self.preprocess(task)
        return test, task

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list, fuel_func=None) -> int:
        """
        Find the number that is linear closest to all numbers in the given list
        Return the total distance between that number and all other numbers

        :param data: List of numbers
        :param fuel_func: Function to calculate the distance (fuel), part 1 uses a linear function
        :return: Minimum linear distance from a number to all other numbers
        """
        if fuel_func is None:
            fuel_func = calculate_fuel
        mean = sum(data) // len(data)
        best_fuel = fuel_func(data, mean)
        direction = 1 if fuel_func(data, mean + 1) < fuel_func(data, mean - 1) else -1
        i = 0
        while True:
            i += direction
            fuel = fuel_func(data, mean + i)
            if fuel < best_fuel:
                best_fuel = fuel
            if fuel > best_fuel:
                break
        return best_fuel

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Find the number that is closest to all numbers in the given list
        Return the total distance between that number and all other numbers

        :param data: List of numbers
        :return: Minimum distance from a number to all other numbers
        """
        return self.part_1(data, calculate_fuel_part_2)


if __name__ == "__main__":
    # Load task
    t = Task7()

    # Run task
    t.run_all()
