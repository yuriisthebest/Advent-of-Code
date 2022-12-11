import math
import operator
from utils.decorators import timer, debug
from utils.task import Task

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '^': operator.xor,
}


class Task11(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 11

    def preprocess(self, data: list) -> list:
        monkeys = []
        for i in range(len(data) // 6):
            monkey = data[i * 7:(i * 7) + 6]
            if not monkey:
                continue
            monkey = {
                "items": list(map(int, "".join(monkey[1][4:]).split(","))),
                "activity": 0,
                "operation": (monkey[2][5], monkey[2][6], monkey[2][7]),
                "test": int(monkey[3][5]),
                "recipient": (int(monkey[4][9]), int(monkey[5][9])),
            }
            monkeys.append(monkey)
        return monkeys

    @staticmethod
    def operation(old: int, op) -> int:
        value1 = old if op[0] == "old" else int(op[0])
        value2 = old if op[2] == "old" else int(op[2])
        return OPS[op[1]](value1, value2)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        for _ in range(20):
            for monkey in data:
                while len(monkey['items']) != 0:
                    monkey['activity'] += 1
                    worry = self.operation(monkey['items'].pop(0), monkey['operation'])
                    worry //= 3
                    new_monkey = monkey['recipient'][0] if worry % monkey['test'] == 0 else monkey['recipient'][1]
                    data[new_monkey]['items'].append(worry)
        return math.prod(sorted([monkey['activity'] for monkey in data], reverse=True)[:2])

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        max_test = math.prod([monkey['test'] for monkey in data])
        for i in range(10000):
            for monkey in data:
                while len(monkey['items']) != 0:
                    monkey['activity'] += 1
                    worry = self.operation(monkey['items'].pop(0), monkey['operation'])
                    worry %= max_test
                    new_monkey = monkey['recipient'][0] if worry % monkey['test'] == 0 else monkey['recipient'][1]
                    data[new_monkey]['items'].append(worry)
        return math.prod(sorted([monkey['activity'] for monkey in data], reverse=True)[:2])


if __name__ == "__main__":
    # Load task
    t = Task11()

    # Run task
    t.run_all()
