from utils.decorators import timer, debug
from utils.task import Task


class Task2(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 2

    def preprocess(self, data: list) -> list:
        return data[0].split(",")

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        result = 0
        for line in data:
            start = int(line.split('-')[0])
            end = int(line.split('-')[1])
            # Iteratively check every number in the specified range
            for i in range(start, end+1):
                word = str(i)
                if len(word) % 2 != 0:
                    continue
                if word[len(word)//2:] == word[:len(word)//2]:
                    result += i
        return result

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        result = 0
        for line in data:
            start = int(line.split('-')[0])
            end = int(line.split('-')[1])
            # Iteratively check every number in the specified range
            for i in range(start, end + 1):
                word = str(i)
                # Check different sizes of repeated numbers
                for chunk_size in range(1, len(word)//2+1):
                    if len(word) % chunk_size != 0:
                        continue
                    chunks = [word[j:j+chunk_size] for j in range(0, len(word), chunk_size)]
                    # Check if there is only 1 unique chunk
                    if len(set(chunks)) == 1:
                        result += i
                        break
        return result


if __name__ == "__main__":
    # Load task
    t = Task2()

    # Run task
    t.run_all()
