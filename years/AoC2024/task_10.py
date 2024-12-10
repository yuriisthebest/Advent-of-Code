from utils.decorators import timer, debug
from utils.task import Task


class Task10(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 10

    def preprocess(self, data: list) -> list:
        return [[int(char) for char in line] for line in data]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list, rating=False) -> int:
        num_trails = 0
        for i, line in enumerate(data):
            for j, char in enumerate(line):
                if char == 0:
                    num_trails += self.find_score_from_head(data, i, j, rating)
        return num_trails

    def find_score_from_head(self, data: list, i: int, j: int, rating: bool = False) -> int:
        current_possibilities = [(i, j)]
        new_possibilities = []
        for i in range(9):
            for pos in current_possibilities:
                for possible_step in self.find_suitable_neighbors(data, *pos):
                    # Overwrite check for any paths vs distinct paths
                    if possible_step not in new_possibilities or rating:
                        new_possibilities.append(possible_step)
            current_possibilities = new_possibilities
            new_possibilities = []
        return len(current_possibilities)

    @staticmethod
    def find_suitable_neighbors(data: list, i: int, j: int) -> list:
        neighbors = []
        height = data[i][j]
        if i > 0 and data[i - 1][j] == height + 1:
            neighbors.append((i - 1, j))
        if j > 0 and data[i][j - 1] == height + 1:
            neighbors.append((i, j - 1))
        if i < len(data) - 1 and data[i + 1][j] == height + 1:
            neighbors.append((i + 1, j))
        if j < len(data[i]) - 1 and data[i][j + 1] == height + 1:
            neighbors.append((i, j + 1))
        return neighbors

    @debug
    def part_2(self, data: list) -> int:
        return self.part_1(data, rating=True)


if __name__ == "__main__":
    # Load task
    t = Task10()

    # Run task
    t.run_all()
