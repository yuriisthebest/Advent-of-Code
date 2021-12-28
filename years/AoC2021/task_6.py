from utils.decorators import timer, debug
from utils.task import Task
from utils.load import load_task_json


class LanternFish:
    """
    Class to simulate a single lantern fish
    """
    def __init__(self, init_timer: int):
        self.timer = init_timer

    def age_day(self):
        """
        Ages the fish a single day, reducing it's internal timer by 1
        The timer is reset to 6 and another fish spawns, if the timer is at 0 when the fish ages
        :return: Nothing or a new fish if it is produced today
        """
        if self.timer == 0:
            self.timer = 6
            return LanternFish(9)
        self.timer -= 1

    def __repr__(self):
        return str(self.timer)


class Task6(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 6

    def load(self) -> tuple:
        test, task = load_task_json(self.YEAR, self.TASK_NUM)
        test = self.preprocess(test)
        task = self.preprocess(task)
        return test, task

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list, days: int = 80) -> int:
        """
        Naive simulation of fish count
        Every fish is simulated individually, their internal timer is reduced by 1 every day

        :param data: The ages of the fish around us
        :param days: The amount of days to simulate the breeding of the fish
        :return: The number of fish after a certain amount of days
        """
        fishes = [LanternFish(time) for time in data]
        for i in range(1, days + 1):
            for fish in fishes:
                new_fish = fish.age_day()
                if new_fish is not None:
                    fishes.append(new_fish)
        return len(fishes)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list, days: int = 256) -> int:
        """
        Fast simulation of fish count
        Fishes are binned on their internal timer and modified as a group

        :param data: The ages of the fish around us
        :param days: The amount of days to simulate the breeding of the fish
        :return: The number of fish after a certain amount of days
        """
        # Setup fish counts of the initial fishes
        fish_counts = [0 for _ in range(9)]
        for num in data:
            fish_counts[num] += 1
        # Simulate every day by moving the counts 1 day down
        #   The count in box 0 is added to box 6 (original fish) and overrides box 8 (new fish)
        for i in range(1, days + 1):
            new_fishes = fish_counts[0]
            for j in range(8):
                fish_counts[j] = fish_counts[j + 1]
            fish_counts[6] += new_fishes
            fish_counts[8] = new_fishes
        return sum(fish_counts)


if __name__ == "__main__":
    # Load task
    t = Task6()

    # Run task
    t.run_all()
