from utils.decorators import timer, debug
from utils.task import Task


class Task8(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 8

    def preprocess(self, data: list) -> list:
        return [list(map(int, row)) for row in data]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        visible_trees = 0
        for i in range(len(data)):
            for j in range(len(data[0])):
                height = data[i][j]
                # Check horizontal rows
                if (all(val < height for val in data[i][:j])
                        or all(val < height for val in data[i][j+1:])):
                    visible_trees += 1
                    continue
                # Check vertical columns
                if (all(data[val][j] < height for val in range(i))
                        or all(data[val][j] < height for val in range(i+1, len(data)))):
                    visible_trees += 1
        return visible_trees

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        max_score = 0
        for i in range(len(data)):
            for j in range(len(data[0])):
                height = data[i][j]
                score = 1
                # Trees to right, left, up, down
                score *= self.seen_trees(height, data[i][j+1:])
                score *= self.seen_trees(height, data[i][:j][::-1])
                score *= self.seen_trees(height, [data[val][j] for val in range(i)][::-1])
                score *= self.seen_trees(height, [data[val][j] for val in range(i+1, len(data))])
                if score > max_score:
                    max_score = score
        return max_score

    @staticmethod
    def seen_trees(height: int, row: list) -> int:
        trees = 0
        for tree in row:
            trees += 1
            if tree >= height:
                break
        return trees


if __name__ == "__main__":
    # Load task
    t = Task8()

    # Run task
    t.run_all()
