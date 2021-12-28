from utils.decorators import timer, debug
from utils.task import Task


class Node:
    def __init__(self, name: str):
        self.name = name
        self.neighbors = []

    def __repr__(self):
        return f"{str(self.name)} ({len(self.neighbors)})"

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def is_big_cave(self):
        return not self.name.islower()


class Task12(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 12

    def preprocess(self, data: list) -> Node:
        nodes = {}
        for path in data:
            name1, name2 = path.split("-")
            if name1 in nodes:
                node1 = nodes[name1]
            else:
                node1 = Node(name1)
                nodes[name1] = node1
            if name2 in nodes:
                node2 = nodes[name2]
            else:
                node2 = Node(name2)
                nodes[name2] = node2
            node1.add_neighbor(node2)
            node2.add_neighbor(node1)
        return nodes['start']

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: Node) -> int:
        return self.find_all_paths(data)

    def find_all_paths(self, data: Node, base_path: list = None) -> int:
        if data.name == "end":
            return 1
        current_path = [] if base_path is None else base_path.copy()
        current_path.append(data)
        num_paths = 0
        for neighbor in data.neighbors:
            if neighbor not in current_path or neighbor.is_big_cave():
                num_paths += self.find_all_paths(neighbor, current_path)
        return num_paths

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: Node) -> int:
        return self.find_all_paths2(data)

    def find_all_paths2(self, data: Node, base_path: list = None) -> int:
        if data.name == "end":
            return 1
        current_path = [] if base_path is None else base_path.copy()
        current_path.append(data)
        num_paths = 0
        for neighbor in data.neighbors:
            if neighbor.is_big_cave() or self.can_add_to_path(current_path, neighbor):
                num_paths += self.find_all_paths2(neighbor, current_path)
        return num_paths

    @staticmethod
    def can_add_to_path(path: list, neighbor) -> bool:
        if neighbor.name == 'start':
            return False
        seen_caves = []
        for node in path:
            if node.is_big_cave():
                continue
            # Two small caves are in the path, only add small cave if it is not in path
            if node in seen_caves:
                return neighbor not in path
            seen_caves.append(node)
        return True


if __name__ == "__main__":
    # Load task
    t = Task12()

    # Run task
    t.run_all()
