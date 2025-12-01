from utils.decorators import timer, debug
from utils.task import Task


class Task1(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 1

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        password = 0
        dial = 50
        for line in data:
            num = int(line[1:])
            # Move dial to the right, increasing the number
            if line[0] == "R":
                dial = (dial + num) % 100
            # Move dial to the left, decreasing the number
            else:
                dial = (dial - num) % 100
            # Stop at 0 means password code increases
            if dial == 0:
                password += 1
        return password

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        password_code = 0
        dial = 50
        for line in data:
            num = int(line[1:])
            password_code += num // 100
            num = num % 100
            # Move dial to the right, increasing the number
            if line[0] == "R":
                dial = dial + num
                # Manually modulo the dial back within range, keeping track of how often
                while dial >= 100:
                    password_code += 1
                    dial -= 100
            # Move dial to the left, decreasing the number
            else:
                # Avoid counting 0's twice
                if dial == 0:
                    password_code -= 1
                dial = dial - num
                # Avoid missing perfect 0's
                if dial == 0:
                    password_code += 1
                # Manually modulo the dial into within range, keeping track of how often
                while dial < 0:
                    password_code += 1
                    dial += 100
        return password_code


if __name__ == "__main__":
    # Load task
    t = Task1()

    # Run task
    t.run_all()
