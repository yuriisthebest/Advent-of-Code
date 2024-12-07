import copy
from utils.decorators import timer, debug
from utils.task import Task


class Task17(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 17

    def preprocess(self, data: list) -> list:
        new_data = []
        for line in data:
            new_data.append([int(num) for num in line])
        return new_data

    @staticmethod
    def manhattan(coord1: tuple, coord2: tuple):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    @staticmethod
    def children(data: list, node: tuple, taken_path: list) -> list:
        children = []
        previous = taken_path[-1]
        horizontal = True
        vertical = True
        if len(taken_path) >= 4:
            if taken_path[-1][0] == taken_path[-2][0] == taken_path[-3][0] == taken_path[-4][0]:
                horizontal = False
            if taken_path[-1][1] == taken_path[-2][1] == taken_path[-3][1] == taken_path[-4][1]:
                vertical = False
        if vertical and 0 <= node[0] + 1 < len(data) and 0 <= node[1] < len(data[0]):
            if (node[0] + 1, node[1]) != previous:
                children.append((node[0] + 1, node[1]))
        if vertical and 0 <= node[0] - 1 < len(data) and 0 <= node[1] < len(data[0]):
            if (node[0] - 1, node[1]) != previous:
                children.append((node[0] - 1, node[1]))
        if horizontal and 0 <= node[0] < len(data) and 0 <= node[1] + 1 < len(data[0]):
            if (node[0], node[1] + 1) != previous:
                children.append((node[0], node[1] + 1))
        if horizontal and 0 <= node[0] < len(data) and 0 <= node[1] - 1 < len(data[0]):
            if (node[0], node[1] - 1) != previous:
                children.append((node[0], node[1] - 1))
        return children

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        seen = []
        end = (len(data) - 1, len(data[0]) - 1)
        todo = [(self.manhattan((0, 0), end), 0, (0, 0), [(0, 0)])]
        while len(todo) != 0:
            _, heat_loss, node, path = todo.pop(0)
            if node == end:
                print(path)
                return heat_loss
            for child in self.children(data, node, path):
                if child in path or child:
                    continue
                if seen.count(child) > 5:
                    continue
                seen.append(child)
                new_heat_loss = heat_loss + data[child[0]][child[1]]
                new_path = copy.deepcopy(path)
                new_path.append(child)
                todo.append((new_heat_loss + self.manhattan(child, end) * 2, new_heat_loss, child, new_path))
            todo.sort(key=lambda x: x[0])
        return len(data)
    # 689 too high

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        return len(data)


if __name__ == "__main__":
    # Load task
    t = Task17()

    # Run task
    t.run_all()
