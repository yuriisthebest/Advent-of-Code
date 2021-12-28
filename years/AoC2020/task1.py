from utils.decorators import timer, debug
import json


@timer
@debug
def find_sum_to(numbers, total):
    for number1 in numbers:
        for number2 in numbers:
            for number3 in numbers:
                if number1 + number2 + number3 == total:
                    return number1 * number2 * number3


if __name__ == "__main__":
    with open("C:\\Users\\Yuri\\Documents\\Python\\Advent of Code\\AoC2021\\task1_input.json") as f:
        nums = json.load(f)
    find_sum_to(nums, 2020)
