import math
from utils.decorators import timer, debug
from utils.task import Task


class Task19(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 19

    def preprocess(self, data: list) -> list:
        blueprints = []
        for line in data:
            blueprints.append((int(line[6]),
                               int(line[12]),
                               (int(line[18]), int(line[21])),
                               (int(line[27]), int(line[30]))))
        return blueprints

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        total_quality = 0
        for i, blueprint in enumerate(data):
            geodes, misc = self.simulate_next_bot(blueprint, 24, (1, 0, 0, 0), (0, 0, 0, 0))
            total_quality += geodes * (i + 1)
        return total_quality

    def simulate_next_bot(self, blueprint: tuple, max_time: int, robots: tuple, resources: tuple):
        """
        Recursion algorithm to simulate the process of building robots
        At each divergence point, choose which bot to build next, then simulate the gather process until it is build

        :param blueprint: The blueprints for the bots
        :param max_time: The amount of time left to build bots
        :param robots: The amount of bots currently active, split into bot types
        :param resources: The amount of resources available from each resource
        :return: The maximal amount of geodes mined from this time point and the amount of bots required
        """
        # Stop the recursion when time runs out
        if max_time <= 0:
            return resources[3], robots
        maximums = max([blueprint[0], blueprint[1], blueprint[2][0], blueprint[3][0]]), blueprint[2][1], blueprint[3][1]
        best_score = 0
        bots = None
        # Four possible bots to build, if useful
        if robots[0] < maximums[0] and robots[0] * max_time + resources[0] < max_time * maximums[0]:
            # Wait to build an ore-bot <+ 1 timeunit to build it>
            waiting_time = 1 + max(0, math.ceil((blueprint[0] - resources[0]) / robots[0]))
            if waiting_time < max_time:
                new_score, new_bots = self.simulate_next_bot(blueprint,
                                                             max_time - waiting_time,
                                                             (robots[0] + 1, robots[1], robots[2], robots[3]),
                                                             (resources[0] + robots[0] * waiting_time - blueprint[0],
                                                              resources[1] + robots[1] * waiting_time,
                                                              resources[2] + robots[2] * waiting_time,
                                                              resources[3] + robots[3] * waiting_time))
                if new_score > best_score:
                    best_score = new_score
                    bots = new_bots
        if robots[1] < maximums[1] and robots[1] * max_time + resources[1] < max_time * maximums[1]:
            # Wait to build a clay-bot
            waiting_time = 1 + max(0, math.ceil((blueprint[1] - resources[0]) / robots[0]))
            if waiting_time < max_time:
                new_score, new_bots = self.simulate_next_bot(blueprint,
                                                             max_time - waiting_time,
                                                             (robots[0], robots[1] + 1, robots[2], robots[3]),
                                                             (resources[0] + robots[0] * waiting_time - blueprint[1],
                                                              resources[1] + robots[1] * waiting_time,
                                                              resources[2] + robots[2] * waiting_time,
                                                              resources[3] + robots[3] * waiting_time))
                if new_score > best_score:
                    best_score = new_score
                    bots = new_bots
        if robots[2] < maximums[2] and robots[1] > 0 and robots[2] * max_time + resources[2] < max_time * maximums[2]:
            # Wait to build an obsidian-bot
            waiting_time = 1 + max([math.ceil((blueprint[2][0] - resources[0]) / robots[0]),
                                    math.ceil((blueprint[2][1] - resources[1]) / robots[1]),
                                    0])
            if waiting_time < max_time:
                new_score, new_bots = self.simulate_next_bot(blueprint,
                                                             max_time - waiting_time,
                                                             (robots[0], robots[1], robots[2] + 1, robots[3]),
                                                             (resources[0] + robots[0] * waiting_time - blueprint[2][0],
                                                              resources[1] + robots[1] * waiting_time - blueprint[2][1],
                                                              resources[2] + robots[2] * waiting_time,
                                                              resources[3] + robots[3] * waiting_time))
                if new_score > best_score:
                    best_score = new_score
                    bots = new_bots
        if robots[2] > 0:
            # Wait to build a geode-bot
            waiting_time = 1 + max([math.ceil((blueprint[3][0] - resources[0]) / robots[0]),
                                    math.ceil((blueprint[3][1] - resources[2]) / robots[2]),
                                    0])
            if waiting_time < max_time:
                new_score, new_bots = self.simulate_next_bot(blueprint,
                                                             max_time - waiting_time,
                                                             (robots[0], robots[1], robots[2], robots[3] + 1),
                                                             (resources[0] + robots[0] * waiting_time - blueprint[3][0],
                                                              resources[1] + robots[1] * waiting_time,
                                                              resources[2] + robots[2] * waiting_time - blueprint[3][1],
                                                              resources[3] + robots[3] * waiting_time))
                if new_score > best_score:
                    best_score = new_score
                    bots = new_bots
        # If no bots can be build anymore, due to nearing the time limit, just simulate the amount of geodes
        if bots is None:
            return resources[3] + max_time * robots[3], robots
        return best_score, bots

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        score = 1
        for i in range(3):
            try:
                blueprint = data[i]
            except IndexError:
                continue
            geodes, misc = self.simulate_next_bot(blueprint, 32, (1, 0, 0, 0), (0, 0, 0, 0))
            score *= geodes
        return score


if __name__ == "__main__":
    # Load task
    t = Task19()

    # Run task
    t.run_all()
