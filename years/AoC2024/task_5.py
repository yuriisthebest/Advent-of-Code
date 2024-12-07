from utils.decorators import timer, debug
from utils.task import Task


class Task5(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 5

    def preprocess(self, data: list) -> list:
        orders = []
        updates = []
        section_one = True
        for line in data:
            if section_one:
                if line == "":
                    section_one = False
                    continue
                orders.append((int(line[:2]), int(line[3:5])))
            else:
                updates.append([int(num) for num in line.split(",")])
        return [orders, updates]

    @staticmethod
    def detect_order(orders: list):
        before = {}
        afters = {}
        for order in orders:
            first = order[0]
            second = order[1]

            if second not in before:
                before[second] = []
            before[second].append(first)

            if first not in afters:
                afters[first] = []
            afters[first].append(second)
        return before, afters

    @staticmethod
    def check_update(update, afters) -> bool:
        seen = []
        for current in update:
            # Check numbers before current
            if current in afters:
                for other_num in seen:
                    if other_num in afters[current]:
                        return False
            # Check numbers after current?
            seen.append(current)
        return True

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        total = 0
        orders, updates = data
        before, afters = self.detect_order(orders)
        for update in updates:
            if self.check_update(update, afters):
                total += update[len(update) // 2]
        return total

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        total = 0
        orders, updates = data
        before, afters = self.detect_order(orders)
        for update in updates:
            if not self.check_update(update, afters):
                update = self.correct_order(before, update)
                total += update[len(update) // 2]
        return total

    def correct_order(self, before: dict, to_dos: list) -> list:
        if len(to_dos) == 0:
            return []
        for current in to_dos:
            # If there are no required numbers before the current, add it in front and find next
            if current not in before:
                to_dos.remove(current)
                return [current, *self.correct_order(before, to_dos)]
            # If there are no required numbers before the current, add it in front and find next
            for num in to_dos:
                if num in before[current]:
                    break
            else:
                to_dos.remove(current)
                return [current, *self.correct_order(before, to_dos)]


if __name__ == "__main__":
    # Load task
    t = Task5()

    # Run task
    t.run_all()
