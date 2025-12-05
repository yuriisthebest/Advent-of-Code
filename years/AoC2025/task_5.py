from utils.decorators import timer, debug
from utils.task import Task


class Task5(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 5

    def preprocess(self, data: list) -> tuple:
        ranges = []
        ids = []
        do_ranges = True
        for line in data:
            if line == '':
                do_ranges = False
                continue
            if do_ranges:
                ranges.append([int(num) for num in line.split('-')])
            else:
                ids.append(int(line))
        return ranges, ids

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: tuple) -> int:
        result = 0
        ranges, ids = data
        for num in ids:
            for up, down in ranges:
                if num in range(up, down+1):
                    result += 1
                    break
        return result

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: tuple) -> int:
        ranges, _ = data
        total_ranges = []
        for new_down, new_up in ranges:
            last_changed = 0
            for i, (down, up) in enumerate(total_ranges):
                # New range starts before the current one
                if new_down < down:
                    # New range also ends before the current one
                    if new_up <= down:
                        total_ranges.insert(i, [new_down, new_up])
                    # New range extends into the current one
                    else:
                        total_ranges[i][0] = new_down
                        # New range exeeds current one, but stops before next
                        if new_up > up:
                            total_ranges[i][1] = new_up
                    last_changed = i
                    break
                # New range starts within current one
                if down <= new_down <= up:
                    if new_up > up:
                        total_ranges[i][1] = new_up
                    last_changed = i
                    break
            else:
                total_ranges.append([new_down, new_up])
            # Combine overlapping ranges
            while last_changed < len(total_ranges) - 1 and total_ranges[last_changed][1] >= total_ranges[last_changed+1][0]:
                removed_down, removed_up = total_ranges.pop(last_changed+1)
                total_ranges[last_changed][1] = max(total_ranges[last_changed][1], removed_up)
        # Calculate the size of each range
        return sum([up-down+1 for down, up in total_ranges])


if __name__ == "__main__":
    # Load task
    t = Task5()

    # Run task
    t.run_all()
