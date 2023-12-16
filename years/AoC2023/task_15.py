from utils.decorators import timer, debug
from utils.task import Task


class Task15(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 15

    @staticmethod
    def hash(string: str):
        value = 0
        for char in string:
            value += ord(char)
            value = (value * 17) % 256
        return value

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        total = 0
        for element in data[0].split(","):
            total += self.hash(element)
        return total

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        boxes = [[] for _ in range(256)]
        for element in data[0].split(","):
            if element[-1] == "-":
                box = self.hash(element[:-1])
                for i, (code, value) in enumerate(boxes[box]):
                    if code == element[:-1]:
                        boxes[box].pop(i)
                        break
            else:
                code, focus = element.split("=")
                box = self.hash(code)
                for i, (c, value) in enumerate(boxes[box]):
                    if c == code:
                        boxes[box][i] = [code, int(focus)]
                        break
                else:
                    boxes[box].append([code, int(focus)])
        total = 0
        for i, box in enumerate(boxes):
            for j, (code, lens) in enumerate(box):
                total += (i+1) * (j+1) * lens
        return total


if __name__ == "__main__":
    # Load task
    t = Task15()

    # Run task
    t.run_all()
