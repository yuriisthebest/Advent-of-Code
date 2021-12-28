from utils.decorators import timer, debug
from utils.task import Task


def perform_program(program, maximum: bool = True):
    """
    Perform the ALU program and maintain possible MODEL numbers

    :param program: The program to run (using concatenated version)
    :param maximum: Whether to return the maximum or minimum number
    :return: The maximum or minimum MODEL number that follows the ALU instructions
    """
    # Z-value: number
    current_possibilities = {0: 0}
    for step_i, step in enumerate(program):
        cutoff = 26**(13-step_i)
        new_possibilities = {}
        # Consider all possibilities, one at a time
        for z in current_possibilities:
            current_num = current_possibilities[z]
            # Add a new digit to all current solutions
            for i in range(9):
                new_w = i + 1
                new_z = program_step(new_w, z, *step)
                # If the z-value is larger than the cutoff, the z-value will never be 0 after the program halts
                if abs(new_z) > cutoff:
                    continue
                # Add the new_z and new number to the possibilities, unless a better number exists with that z
                if (new_z not in new_possibilities
                        or gt_or_lt(current_num*10+new_w, new_possibilities[new_z], maximum)):
                    new_possibilities[new_z] = current_num*10 + new_w
        # print(f"({step_i}) Considering {len(new_possibilities)} solutions")  # Nice debug statement
        current_possibilities = new_possibilities
    return current_possibilities


def gt_or_lt(value1, value2, op):
    """
    :return: value1 > value2 if op else value 1 < value2
    """
    if op:
        return value1 > value2
    return value1 < value2


def program_step(w: int, z: int, divider: int, add_x: int, add_y: int):
    # Each section of [my input] program can be described as the following computations, reducing computation time
    x = z % 26
    z = z // divider
    x += add_x
    if x == w:
        z = z
    else:
        z = 26*z + w + add_y
    return z


class Task24(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 24

    def preprocess(self, data: list) -> list:
        if len(data) <= 1:
            return []
        new_program = []
        for i in range(14):
            divider = data[i * 18 + 4]
            add_x = data[i * 18 + 5]
            add_y = data[i * 18 + 15]
            new_program.append([int(divider[2]), int(add_x[2]), int(add_y[2])])
        return new_program

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        if len(data) <= 1:
            return 0
        result = perform_program(data)
        return result[0]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        if len(data) <= 1:
            return 0
        result = perform_program(data, False)
        return result[0]


if __name__ == "__main__":
    # Load task
    t = Task24()

    # Run task
    t.run_all()
