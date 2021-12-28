from utils.decorators import timer, debug
from utils.task import Task

# Task constants
TABLE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}
TABLE2 = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}
OPENINGS = ["(", "[", "{", "<"]
EXPECTED = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}


def find_illegal_character(line: str):
    """
    Please don't look at this
    It works, don't ask me which lines can be removed

    :param line: String of bracket characters
    :return: None if the line is legal, else the first illegal character
    """
    start = line[0]
    to_i = 0
    for i, char in enumerate(line):
        if i <= to_i:
            continue
        if line[i] in OPENINGS:
            # Analyze sub-string with a new starting character
            result, new_i = find_illegal_character(line[i:])
            to_i = i + new_i
            if result is not None:
                return result, i
        elif line[i] == EXPECTED[start]:
            return None, i
        else:
            # Found mistake
            return line[i], i
    return None, 0


def find_incomplete(line: str, start_i: int = 0):
    """
    Recursive function to determine which brackets are required to complete the line

    :param line: String of bracket characters
    :param start_i: Integer to keep track of the position of the program in the line
    :return: List of characters required to complete the line, in order
    """
    completion = []
    start = line[start_i]
    to_i = start_i
    for i in range(start_i, len(line)):
        if i <= to_i:
            continue
        if line[i] in OPENINGS:
            # Analyze sub-string with a new starting character
            result, to_i = find_incomplete(line, i)
            if result is not None:
                completion.extend(result)
        elif line[i] == EXPECTED[start]:
            # Found the closing bracket!
            if start_i == 0 and i != len(line):
                # Continue if this is the main loop and not all characters have been checked
                result, i = find_incomplete(line, i+1)
                completion.extend(result)
            return completion, i
    # Closing character not found, adding character to output list
    completion.append(EXPECTED[start])
    return completion, len(line)


class Task10(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 10

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        """
        Check each line in the data for corruption

        :param data: List of strings with bracket characters
        :return: Total score of corrupted characters
        """
        score = 0
        for line in data:
            result, _ = find_illegal_character(line)
            if result is not None:
                score += TABLE[result]
        return score

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Check each line in the data for incompleteness

        :param data: List of strings with bracket characters
        :return: Middle score of incomplete lines
        """
        scores = []
        for line in data:
            # Ignore corrupted lines
            result, _ = find_illegal_character(line)
            if result is not None:
                continue
            result, _ = find_incomplete(line)
            # Calculate game score of incomplete lines
            score = 0
            for char in result:
                score *= 5
                score += TABLE2[char]
            if score != 0:
                scores.append(score)
        scores.sort()
        return scores[len(scores) // 2]


if __name__ == "__main__":
    # Load task
    t = Task10()

    # Run task
    t.run_all()
