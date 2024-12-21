from functools import cache
from utils.decorators import timer, debug
from utils.task import Task


class Task21(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 21

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        complexity = 0
        for code in data:
            number = int(code[:-1])
            code = self.give_orders([code])
            code = self.give_orders(code)
            code = self.give_orders(code)
            length = sum([len(chain) for chain in code])
            complexity += number * length
        return complexity

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        complexity = 0
        for code in data:
            number = int(code[:-1])
            code = [code]
            for i in range(26):
                print(i, len(code))
                code = self.give_orders(code)
            # print(len(code), code)
            length = sum([len(chain) for chain in code])
            complexity += number * length
        return complexity

    @staticmethod
    def get_coord(value: chr) -> tuple:
        if isinstance(value, int):
            return (value - 1) // 3, (value - 1) % 3 if value != 0 else 1
        else:
            match value:
                case "A":
                    return -1, 2
                case "^":
                    return -1, 1
                case "<":
                    return -2, 0
                case "v":
                    return -2, 1
                case ">":
                    return -2, 2

    @cache
    def steps_numeric(self, start: chr, end: chr):
        start_coord = self.get_coord(start)
        end_coord = self.get_coord(end)
        path = ""
        # Go left as needed
        path += "<" * max(0, start_coord[1] - end_coord[1])
        # Go up or down as needed
        path += "^" * max(0, end_coord[0] - start_coord[0])
        path += "v" * max(0, start_coord[0] - end_coord[0])
        # Go right as needed
        path += ">" * max(0, end_coord[1] - start_coord[1])
        # If the path goes through the blank (at -1, 0). Reverse the path to not do that
        if (start_coord[0] == -1 and end_coord[1] == 0) or end_coord[0] == -1 and start_coord[1] == 0:
            path = path[::-1]
        return path

    @cache
    def do_chain(self, chain: str) -> list:
        orders = []
        current_node = "A"
        for key in chain:
            try:
                key = int(key)
            except ValueError:
                pass
            path = self.steps_numeric(current_node, key)
            current_node = key
            path += "A"
            orders.append(path)
        return orders

    def give_orders(self, code: list) -> list:
        orders = []
        for chain in code:
            chains = self.do_chain(chain)
            orders.extend(chains)
        return orders


if __name__ == "__main__":
    # Load task
    t = Task21()

    # Run task
    t.run_all()
