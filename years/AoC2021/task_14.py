from utils.decorators import timer, debug
from utils.task import Task
import numpy as np


class Task14(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 14

    def preprocess(self, data: list) -> list:
        """
        Process list of element template and pair insertions into a dictionary for the pair insertions

        :param data: Input list
        :return: List with two elements, the string template and dictionary pair insertions
        """
        template = data[0]
        insertions = {}
        for insertion in data[2:]:
            insertions[insertion[0]] = insertion[2]
        return [template, insertions]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        """
        Perform 10 element insertions on a given input template

        :param data: List with two elements, the string template and dictionary pair insertions
        :return: The difference between the amount of most common and least common elements
        """
        template = data[0]
        # Perform 10 steps of element insertions
        for _ in range(10):
            new_polymer = template[0]
            # Check each pair of characters in the string
            for s1, s2 in zip(template, template[1:]):
                new_polymer += data[1][s1 + s2]
                new_polymer += s2
            template = new_polymer
        # Count all characters in the final element template
        counts = {char: 0 for char in set(template)}
        for char in template:
            counts[char] += 1
        return max(counts.values()) - min(counts.values())

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Perform 40 element insertions on a given input template

        :param data: List with two elements, the string template and dictionary pair insertions
        :return: The difference between the amount of most common and least common elements
        """
        # Initialize count of pairs
        counts = {pair: 0 for pair in set(data[1])}
        for s1, s2 in zip(data[0], data[0][1:]):
            counts[s1 + s2] += 1
        # Perform 40 steps of element insertions
        for _ in range(40):
            new_count = {pair: 0 for pair in set(data[1])}
            for pair in counts:
                inserted = data[1][pair]
                new_count[pair[0] + inserted] += counts[pair]
                new_count[inserted + pair[1]] += counts[pair]
            counts = new_count
        # Find most and least common elements
        element_count = {char: 0 for char in set(data[1].values())}
        for pair in counts:
            element_count[pair[0]] += counts[pair]
            element_count[pair[1]] += counts[pair]
        element_count = {elem: int(np.ceil(element_count[elem] / 2)) for elem in element_count}
        return max(element_count.values()) - min(element_count.values())


if __name__ == "__main__":
    # Load task
    t = Task14()

    # Run task
    t.run_all()
