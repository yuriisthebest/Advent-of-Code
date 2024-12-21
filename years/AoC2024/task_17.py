from utils.decorators import timer, debug
from utils.task import Task


class Task17(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 17

    def preprocess(self, data: list) -> list:
        return [[int(data[0][2]), int(data[1][2]), int(data[2][2])], [int(num) for num in data[4][1].split(",")]]

    @staticmethod
    def process_operation(opcode: int, operand: int, register: list, pointer: int) -> tuple:
        output = -1
        combo_operand = (operand if operand <= 3 else
                         register[0] if operand == 4 else
                         register[1] if operand == 5 else
                         register[2])
        match opcode:
            case 0:
                register[0] = int(register[0] / 2 ** combo_operand)
            case 1:
                register[1] = register[1] ^ operand
            case 2:
                register[1] = combo_operand % 8
            case 3:
                if register[0] != 0 and pointer != operand:
                    pointer = operand - 2
            case 4:
                register[1] = register[1] ^ register[2]
            case 5:
                output = combo_operand % 8
            case 6:
                register[1] = int(register[0] / 2 ** combo_operand)
            case 7:
                register[2] = int(register[0] / 2 ** combo_operand)
        return register, pointer + 2, output

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> str:
        output = self.run_program(*data)
        return ",".join([str(num) for num in output])

    def run_program(self, register: list, program: list):
        pointer = 0
        output = []
        while pointer < len(program):
            register, pointer, out = self.process_operation(program[pointer], program[pointer + 1], register, pointer)
            if out != -1:
                output.append(out)
        return output

    def debug_program(self, register: list, program: list):
        pointer = 0
        output = []
        orders = []
        while pointer < len(program):
            orders.append((program[pointer], program[pointer + 1], register.copy(), pointer))
            register, pointer, out = self.process_operation(program[pointer], program[pointer + 1], register, pointer)
            if out != -1:
                output.append(out)
        return output, orders

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Decoded program
        1(2, 4) -> B = A % 8	-> B is 3 bit
        2(1, 1) -> B = B XOR 1	-> 1st bit of B is flipt
        3(7, 5) -> C = A/B	    -> ?
        4(4, 7) -> B = B XOR C	-> ?
        5(1, 4) -> B = B XOR 4	-> 3rd bit of B is flipt
        6(0, 3) -> A = A/3	    -> A is reduced
        7(5, 5) -> output B % 8	-> print B
        8(3, 0) -> if A != 0, goto start, else just stop

        :param data: The initial register and the program to mimic
        :return: The value of register A that is required to make the program output itself
        """
        if len(data[1]) > 8:
            return 0
        _, program = data
        output = ""
        i = 8**15 if len(program) == 16 else 0
        while output != program:
            i += 1
            register = data[0].copy()
            register[0] = i
            output = self.run_program(register, program)
            # print(i, output, bin(i))
        return i


if __name__ == "__main__":
    # Load task
    t = Task17()

    # Run task
    t.run_all()
