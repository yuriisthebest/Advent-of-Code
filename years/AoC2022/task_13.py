from utils.decorators import timer, debug
from utils.task import Task
from utils import load


class Task13(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 13

    def load(self) -> tuple:
        test, task = load.load_task_json(self.YEAR, self.TASK_NUM)
        test = self.preprocess(test)
        task = self.preprocess(task)
        return test, task

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        sum_correct_order = 0
        for pair in range(len(data)//2):
            packet1 = data[pair*2]
            packet2 = data[pair*2+1]
            if self.correct_order(packet1, packet2):
                sum_correct_order += pair + 1
        return sum_correct_order

    def correct_order(self, packet1: list or int, packet2: list or int) -> bool or None:
        # Compare two values
        if type(packet1) == int and type(packet2) == int:
            if packet1 == packet2:
                return None
            return packet1 < packet2
        # Convert integers to lists (if present)
        packet1 = [packet1] if type(packet1) == int else packet1
        packet2 = [packet2] if type(packet2) == int else packet2
        # Check values from lists
        for value1, value2 in zip(packet1, packet2):
            result = self.correct_order(value1, value2)
            if result is None:
                continue
            return result
        # Compare list lengths
        return self.correct_order(len(packet1), len(packet2))

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        divider1 = [[2]]
        divider2 = [[6]]
        data.append(divider1)
        data.append(divider2)
        # Insertion sort
        order = []
        for packet in data:
            for i, other_packet in enumerate(order):
                if self.correct_order(packet, other_packet):
                    order.insert(i, packet)
                    break
            else:
                order.append(packet)
        return (order.index(divider1) + 1) * (order.index(divider2) + 1)


if __name__ == "__main__":
    # Load task
    t = Task13()

    # Run task
    t.run_all()
