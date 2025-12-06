from utils.decorators import timer, debug
from utils.task import Task
from utils.load import load_task


class Task6(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 6

    def load(self) -> tuple:
        test, task = load_task(custom_loader, "txt", self.YEAR, self.TASK_NUM)
        test = self.preprocess(test)
        task = self.preprocess(task)
        return test, task

    def preprocess(self, data: list) -> list:
        """
        The input data looks like:
        num1-p1 num1-p2 num1-p3
        num2-p1 num2-p2 num2-p3
        num3-p1 num3-p2 num3-p3

        It has to go to
        [[num1-p1, num2,p1, num3-p1], [num1-p2, num2,p2, num3-p2], [num1-p3, num2,p3, num3-p3]]
        """
        problems = []
        for j, line in enumerate(data):
            # Keep track of pX
            problem_id = 0
            for i, char in enumerate(line):
                # Found break in the numbers, go to next problem number
                if char == " " and all([data[x][i] == " " for x in range(4)]):
                    problem_id += 1
                    continue
                # Add the next character to the current number of the current problem
                self.add_char(char, j, problem_id, problems)
        return problems

    @staticmethod
    def add_char(char, num_id, problem_id, problems):
        """
        Add a character to the current number of the current problem
        """
        # Add problems and/or numbers if there are currently no indexes for it
        if len(problems) <= problem_id:
            problems.append([])
        if len(problems[problem_id]) <= num_id:
            problems[problem_id].append("")
        problems[problem_id][num_id] += char

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        result = 0
        for line in data:
            # Convert string number into ints
            nums = [int(i) for i in line[:-1]]
            # Summation
            if line[-1].strip(" ") == "+":
                result += sum(nums)
            # Product
            else:
                res = 1
                for num in nums:
                    res *= num
                result += res
        return result

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        result = 0
        for problem in data:
            # Read the problem numbers from the column and convert to regular ints
            max_length = max([len(num) for num in problem[:-1]])
            nums = [[] for _ in range(max_length)]
            # Iteratively go over each digit to add it to the correct number
            for num in problem[:-1]:
                num_length = len(num)
                for i, digit in enumerate(num):
                    nums[num_length-i-1].append(digit)
            # Reuse part 1
            nums = [int("".join(num)) for num in nums]
            if problem[-1].strip(" ") == "+":
                result += sum(nums)
            else:
                res = 1
                for num in nums:
                    res *= num
                result += res
        return result


def custom_loader(file_path: str):
    """
    Load a txt file

    :param file_path: Path to file to load
    :return: Data from txt in formatted list
    """
    with open(file_path) as f:
        data = []
        for line in f:
            line = line.strip("\n")
            # REMOVED THE LINE THAT SPLIT ON WHITESPACE
            if len(line) == 1:
                line = line[0]
            data.append(line)
    return data


if __name__ == "__main__":
    # Load task
    t = Task6()

    # Run task
    t.run_all()
