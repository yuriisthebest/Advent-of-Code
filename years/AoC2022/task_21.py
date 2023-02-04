from utils.decorators import timer, debug
from utils.task import Task


class Task21(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 21

    def preprocess(self, data: list) -> dict:
        return {line[0][:-1]: line[1:] if len(line[1:]) > 1 else int(line[1]) for line in data}

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: dict) -> int:
        return self.process_monkey(data, "root")

    def process_monkey(self, monkeys: dict, monkey: str) -> int:
        if monkey == "humn":
            return monkeys[monkey]
        if isinstance(monkeys[monkey], int):
            return monkeys[monkey]
        monkey1 = self.process_monkey(monkeys, monkeys[monkey][0])
        monkey2 = self.process_monkey(monkeys, monkeys[monkey][2])
        return int(eval(f"{monkey1} {monkeys[monkey][1]} {monkey2}"))

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: dict) -> int:
        root_monkey = "root"
        target = "humn"
        data[root_monkey][1] = "="
        # Find on which equation path the human lies and determine what the final score should be
        path = self.path_to_monkey(data, root_monkey, target)
        score = None
        for i, step in enumerate(path):
            if step == target:
                return score
            # Calculate the score of the known side
            other_side = data[step][0] if data[step][0] != path[i+1] else data[step][2]
            other_side = self.process_monkey(data, other_side)
            # Determine what the 'unknown' side should be to solve the equation
            match data[step][1]:
                case "+":
                    score -= other_side
                case "-":
                    # Check which side of the minus the human is on
                    if data[step][0] == path[i+1]:
                        score += other_side
                    else:
                        score = other_side - score
                case "*":
                    score /= other_side
                    score = int(score)
                case "/":
                    # Check which side of the divide the human is on
                    if data[step][0] == path[i + 1]:
                        score *= other_side
                    else:
                        score = other_side / score
                case "=":
                    score = other_side

    def path_to_monkey(self, monkeys: dict, source: str, target: str) -> list or None:
        if isinstance(monkeys[source], int):
            if source == target:
                return [target]
            return None
        monkey1 = self.path_to_monkey(monkeys, monkeys[source][0], target)
        monkey2 = self.path_to_monkey(monkeys, monkeys[source][2], target)
        result = None
        if monkey1 is not None:
            result = monkey1
            result.insert(0, source)
        if monkey2 is not None:
            result = monkey2
            result.insert(0, source)
        return result


if __name__ == "__main__":
    # Load task
    t = Task21()

    # Run task
    t.run_all()
