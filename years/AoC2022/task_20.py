from utils.decorators import timer, debug_shape
from utils.task import Task


class Node:
    def __init__(self, num: int, previous):
        self.value = num
        self.left = previous
        self.right = None

    def __repr__(self) -> str:
        return f"<{self.left.value}:{self.value}:{self.right.value}>"

    def move(self, max_steps: int = None):
        """
        Move the node to the left or right in the sequence, depending on the value
        """
        # Let the old neighbors point to each other
        self.left.right = self.right
        self.right.left = self.left
        # Find the new left neighbor
        new_left_neighbor = self.left
        steps = abs(self.value) % (max_steps - 1) if self.value > 0 else (abs(self.value)) % (max_steps - 1)
        for _ in range(steps):
            if self.value > 0:
                new_left_neighbor = new_left_neighbor.right
            else:
                new_left_neighbor = new_left_neighbor.left
        # Set the pointers correct
        new_right_neighbor = new_left_neighbor.right
        new_left_neighbor.right = self
        new_right_neighbor.left = self
        self.right = new_right_neighbor
        self.left = new_left_neighbor


class Task20(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 20

    def preprocess(self, data: list) -> list:
        new_data = []
        prev = None
        for num in data:
            new_node = Node(int(num), prev)
            new_data.append(new_node)
            try:
                prev.right = new_node
            except AttributeError:
                pass
            prev = new_node
        new_data[0].left = prev
        prev.right = new_data[0]
        return new_data

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        # Mix all numbers
        for node in data:
            node.move(len(data))
        return self.calculate_score(data)

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        key = 811589153
        for node in data:
            node.value *= key
        # Mix the numbers 10 times
        for i in range(10):
            for node in data:
                node.move(len(data))
        return self.calculate_score(data)

    @staticmethod
    def calculate_score(data):
        # Find the starting point
        starting_point = None
        for node in data:
            if node.value == 0:
                starting_point = node
                break
        # Find the cords
        score = 0
        current_node = starting_point
        for i in range(3000):
            current_node = current_node.right
            if i % 1000 == 999:
                score += current_node.value
        return score


if __name__ == "__main__":
    # Load task
    t = Task20()

    # Run task
    t.run_all()
