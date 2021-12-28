from utils.decorators import timer, debug
from utils.task import Task
from utils.load import load_task_json
import numpy as np
from copy import deepcopy


class Node:
    def __init__(self, fish_num, parent):
        self.parent = parent
        if isinstance(fish_num, int):
            self.value = fish_num
            self.leaf = True
        if isinstance(fish_num, list):
            self.leaf = False
            self.left = fish_num[0] if isinstance(fish_num[0], Node) else Node(fish_num[0], self)
            self.right = fish_num[1] if isinstance(fish_num[1], Node) else Node(fish_num[1], self)

    @property
    def is_leaf(self) -> bool:
        return self.leaf

    def split(self):
        """
        Split the node into two values with at most 1 difference, summing to the original value of this node
        The left value is the lower value
        """
        self.leaf = False
        self.left = Node(int(np.floor(self.value/2)), self)
        self.right = Node(int(np.ceil(self.value / 2)), self)
        self.value = None

    def explode(self):
        """
        Explode the node, adding its left value to the left closest node and the right value to the right closest node
        This node then turns into a leaf with value 0
        """
        left_node = self.find_left_neighbor(self)
        right_node = self.find_right_neighbor(self)
        if left_node is not None:
            left_node.value += self.left.value
        if right_node is not None:
            right_node.value += self.right.value
        # Change exploded Node into leaf with value 0
        self.value = 0
        self.leaf = True
        self.left = None
        self.right = None

    @staticmethod
    def find_left_neighbor(node: 'Node'):
        """
        Find the closest node to the left of the given node
        """
        next_node = node.parent
        while next_node.left == node:
            node = next_node
            next_node = node.parent
            # There is no left neighbor
            if next_node is None:
                return None
        node = next_node.left
        while not node.is_leaf:
            node = node.right
        return node

    @staticmethod
    def find_right_neighbor(node: 'Node'):
        """
        Find the closest node to the right of the given node
        """
        next_node = node.parent
        while next_node.right == node:
            node = next_node
            next_node = node.parent
            # There is no right neighbor
            if next_node is None:
                return None
        node = next_node.right
        while not node.is_leaf:
            node = node.left
        return node

    def __repr__(self):
        if self.is_leaf:
            return f"{self.value}"
        return f"[{self.left}, {self.right}]"

    def __add__(self, other):
        new_node = Node([self, other], None)
        self.parent = new_node
        other.parent = new_node
        return new_node


class Task18(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 18

    def load(self) -> tuple:
        test, task = load_task_json(self.YEAR, self.TASK_NUM)
        test = self.preprocess(test)
        task = self.preprocess(task)
        return test, task

    def preprocess(self, data: list) -> list:
        """
        Process each snailfish number from nested lists into a tree structure

        :param data: List of snailfish numbers, which are nested lists with 2 elements each
        :return: List of snailfish numbers, each snailfish number is represented by the root of their tree structure
        """
        output = []
        for fish_num in data:
            output.append(Node(fish_num, None))
        return output

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        """
        Calculate the magnitude of the sum of the given snailfish numbers

        :param data: List of snailfish numbers, each snailfish number is represented by the root of their tree structure
        :return: Magnitude of the final sum of all the snailfish numbers
        """
        final_sum = None
        for fish_num in data:
            final_sum = self.add_snailfish_nums(final_sum, fish_num)
        return self.compute_magnitude(final_sum)

    def add_snailfish_nums(self, num1: Node, num2: Node) -> Node:
        """
        Take two snailfish numbers and add them together
            First, merge the two numbers into one list, then reduce this list to get a valid snailfish number

        :param num1: Snailfish number
        :param num2: Snailfish number
        :return: Snailfish number
        """
        # Base case for the first number
        if num1 is None:
            return num2
        new_node = num1 + num2
        # Explode or split the fish number until it doesn't change
        changed = True
        while changed:
            changed = self.find_explosion(new_node)
            if changed is False:
                changed = self.find_split(new_node)
        return new_node

    def find_explosion(self, num: Node, depth: int = 0) -> bool:
        # Base cases for nodes that are leafs or that should be exploded
        if num.is_leaf:
            return False
        if depth == 4:
            num.explode()
            return True
        result = self.find_explosion(num.left, depth+1)
        if result:
            return True
        result = self.find_explosion(num.right, depth+1)
        if result:
            return True
        return False

    def find_split(self, num: Node) -> bool:
        # Base cases for leaf nodes that should or should not be split
        if num.is_leaf and num.value > 9:
            num.split()
            return True
        if num.is_leaf:
            return False
        change = self.find_split(num.left)
        if change is True:
            return True
        change = self.find_split(num.right)
        if change is True:
            return True
        return False

    def compute_magnitude(self, num: Node) -> int:
        """
        Recursively compute the magnitude of a given snailfish number

        :return: Magnitude of given snailfish number
        """
        if num.is_leaf:
            return num.value
        return 3 * self.compute_magnitude(num.left) + 2 * self.compute_magnitude(num.right)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Find the largest magnitude by adding two snailfish numbers together from the list of given snailfish numbers

        :param data: List of snailfish numbers, each snailfish number is represented by the root of their tree structure
        :return: The largest magnitude
        """
        max_num = 0
        for num1 in data:
            for num2 in data:
                # Only add different numbers
                if num1 == num2:
                    continue
                number = self.add_snailfish_nums(deepcopy(num1), deepcopy(num2))
                value = self.compute_magnitude(number)
                if value > max_num:
                    max_num = value
        return max_num


if __name__ == "__main__":
    # Load task
    t = Task18()

    # Run task
    t.run_all()
