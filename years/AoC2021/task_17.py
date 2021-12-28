from utils.decorators import timer, debug
from utils.task import Task


class Task17(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 17

    def preprocess(self, data: list) -> list:
        """
        :param data: Input from task
        :return: Ranges of the target area [[min x, max x], [min y, max y]]
        """
        x = [int(value.replace(",", "")) for value in data[0][2].split('=')[-1].split('..')]
        y = [int(value.replace(",", "")) for value in data[0][3].split('=')[-1].split('..')]
        return [x, y]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        """
        Find trajectory with highest y position

        :param data: Ranges of the target area [[min x, max x], [min y, max y]]
        :return: Highest possible y position
        """
        max_y = 0
        for velocity_x in range(100):
            for velocity_y in range(100):
                top_y = self.simulate_trajectory(velocity_x, velocity_y, data)
                if top_y > max_y:
                    max_y = top_y
        return max_y

    @staticmethod
    def in_region(position, target) -> bool:
        if position[0] in range(target[0][0], target[0][1]+1) and position[1] in range(target[1][0], target[1][1]+1):
            return True
        return False

    def simulate_trajectory(self, v_x, v_y, target) -> int:
        pos = [0, 0]
        max_y = 0
        # Simulate until the probe is in th target (or the probe has missed)
        while not self.in_region(pos, target):
            # Update position
            pos[0] += v_x
            pos[1] += v_y
            # Update velocities
            v_y -= 1
            if v_x != 0:
                v_x -= 1 if v_x > 0 else -1
            if pos[1] > max_y:
                max_y = pos[1]
            # Missed the target
            if pos[1] < target[1][0]:
                return -1
        return max_y

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Find the amount of initial velocities that reach the target area

        :param data: Ranges of the target area [[min x, max x], [min y, max y]]
        """
        num_velocities = 0
        for velocity_x in range(400):
            for velocity_y in range(-100, 100):
                top_y = self.simulate_trajectory(velocity_x, velocity_y, data)
                # If the top is above -1, the trajectory completes
                if top_y > -1:
                    num_velocities += 1
        return num_velocities


if __name__ == "__main__":
    # Load task
    t = Task17()

    # Run task
    t.run_all()
