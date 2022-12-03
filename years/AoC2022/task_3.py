from utils.decorators import timer, debug
from utils.task import Task


def get_priority(common_items: set):
    priorities = 0
    for item in common_items:
        item_prio = ord(item) - 96
        if item_prio < 0:
            item_prio += 58
        priorities += item_prio
    return priorities


class Task3(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 3

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        prio = 0
        for backpack in data:
            compartment1 = set(backpack[:len(backpack)//2])
            compartment2 = set(backpack[len(backpack) // 2:])
            common = compartment1.intersection(compartment2)
            prio += get_priority(common)
        return prio

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        prio = 0
        for i in range(len(data)//3):
            group = data[i*3:(i*3)+3]
            common_items = set(group[0]).intersection(set(group[1])).intersection(set(group[2]))
            prio += get_priority(common_items)
        return prio


if __name__ == "__main__":
    # Load task
    t = Task3()

    # Run task
    t.run_all()
