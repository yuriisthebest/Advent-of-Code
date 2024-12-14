from utils.decorators import timer, debug
from utils.task import Task


class Task14(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 14

    def preprocess(self, data: list) -> list:
        bots = []
        for line in data:
            bot_pos = line[0].split(",")
            bot_pos = [int(bot_pos[0][2:]), int(bot_pos[1])]
            bot_v = line[1].split(",")
            bot_v = (int(bot_v[0][2:]), int(bot_v[1]))
            bots.append([bot_pos, bot_v])
        return bots

    @staticmethod
    def location_after_x_steps(bot: list, steps: int, width: int, height: int):
        return ((bot[0][0] + steps * bot[1][0]) % width,
                (bot[0][1] + steps * bot[1][1]) % height)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        if len(data) < 20:
            width, height = 11, 7
        else:
            width, height = 101, 103
        end_positions = []
        for bot in data:
            end_positions.append(self.location_after_x_steps(bot, 100, width, height))
        # Find quadrants
        quadrant = [[] for _ in range(4)]
        for pos in end_positions:
            index = 0
            if pos[0] == width // 2 or pos[1] == height // 2:
                continue
            if pos[0] > width // 2:
                index += 2
            if pos[1] > height // 2:
                index += 1
            quadrant[index].append(pos)
        return len(quadrant[0]) * len(quadrant[1]) * len(quadrant[2]) * len(quadrant[3])

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        if len(data) < 20:
            return 0
        width, height = 101, 103
        for i in range(width * height)[::-1]:
            end_positions = []
            for bot in data:
                end_positions.append(self.location_after_x_steps(bot, i, width, height))
            # Check if the bots possibly form a frame of the Christmas tree
            for pos in end_positions:
                for j in range(1, 8):
                    if (pos[0], pos[1] + j) not in end_positions:
                        break
                else:
                    return i
        return 0


if __name__ == "__main__":
    # Load task
    t = Task14()

    # Run task
    t.run_all()
