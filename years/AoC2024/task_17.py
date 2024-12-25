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
        """
        _, program = data
        result = self.find_next_digit(program, "")
        return int(result, 8)

    def find_next_digit(self, program: list, octo: oct) -> str | bool:
        for i in range(8):
            if octo == "" and i == 0:
                continue
            new_octo = octo + str(i)
            p_result = self.run_program([int(new_octo, 8), 0, 0], program)

            # Stop the search if we have found the input that creates the program
            if p_result == program:
                return new_octo

            # If this part of the program is recreated, try to increase the register to find the next
            if p_result == program[-len(p_result):]:
                next_digit = self.find_next_digit(program, new_octo)
                # Only return if the digits after have returned, thus the answer is found
                if next_digit is not False:
                    return next_digit
        return False


if __name__ == "__main__":
    # Load task
    t = Task17()

    # Run task
    t.run_all()
