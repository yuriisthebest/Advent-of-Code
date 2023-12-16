from utils.decorators import timer, debug
from utils.task import Task


class Task14(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 14

    def preprocess(self, data: list) -> dict:
        new_data = {}
        for i, line in enumerate(data):
            new_data[i] = {j: char if char != "." else None for j, char in enumerate(line)}
        return new_data

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: dict) -> int:
        data = self.tilt(data, "North")
        return self.compute_load(data)

    @staticmethod
    def compute_load(data: dict) -> int:
        load = 0
        for i, line in data.items():
            for char in line.values():
                if char == "O":
                    load += len(data) - i
        return load

    def tilt(self, platform: dict, side: str) -> dict:
        if side == "North":
            plat = platform.items()
            fun = self.move_up
        elif side == "West":
            plat = platform.items()
            fun = self.move_left
        elif side == "South":
            plat = list(platform.items())[::-1]
            fun = self.move_down
        else:
            plat = platform.items()
            fun = self.move_right
        for i, line in plat:
            if side == "East":
                line = list(line.items())[::-1]
            else:
                line = line.items()
            for j, element in line:
                if element == "O":
                    platform = fun(platform, (i, j))
        return platform

    def move_up(self, platform: dict, stone: tuple) -> dict:
        if stone[0] == 0:
            return platform
        if platform[stone[0] - 1][stone[1]] is None:
            platform[stone[0] - 1][stone[1]] = "O"
            platform[stone[0]][stone[1]] = None
            self.move_up(platform, (stone[0] - 1, stone[1]))
        return platform

    def move_down(self, platform: dict, stone: tuple) -> dict:
        if stone[0] >= len(platform) - 1:
            return platform
        if platform[stone[0] + 1][stone[1]] is None:
            platform[stone[0] + 1][stone[1]] = "O"
            platform[stone[0]][stone[1]] = None
            self.move_down(platform, (stone[0] + 1, stone[1]))
        return platform

    def move_right(self, platform: dict, stone: tuple) -> dict:
        if stone[1] >= len(platform[0]) - 1:
            return platform
        if platform[stone[0]][stone[1] + 1] is None:
            platform[stone[0]][stone[1] + 1] = "O"
            platform[stone[0]][stone[1]] = None
            self.move_right(platform, (stone[0], stone[1] + 1))
        return platform

    def move_left(self, platform: dict, stone: tuple) -> dict:
        if stone[1] == 0:
            return platform
        if platform[stone[0]][stone[1] - 1] is None:
            platform[stone[0]][stone[1] - 1] = "O"
            platform[stone[0]][stone[1]] = None
            self.move_left(platform, (stone[0], stone[1] - 1))
        return platform

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: dict) -> int:
        # Loop sizes found manually
        loop_size = 26 if data[0][0] == "#" else 7
        state = [self.save_data(data)]
        for i in range(1000000000):
            data = self.tilt(data, "North")
            data = self.tilt(data, "West")
            data = self.tilt(data, "South")
            data = self.tilt(data, "East")
            new_state = self.save_data(data)
            if new_state in state:
                if state.index(new_state) % loop_size == 1000000000 % loop_size:
                    return self.compute_load(data)
            state.append(new_state)

    @staticmethod
    def save_data(data):
        state = ""
        for i, line in data.items():
            for j, char in line.items():
                if char == "O":
                    state += f"{i}{j} "
            state += "  "
        return state


if __name__ == "__main__":
    # Load task
    t = Task14()

    # Run task
    t.run_all()
