from utils.decorators import timer, debug
from utils.task import Task


class Task2(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 2

    SHAPE_SCORE = {
        'X': 1,
        'Y': 2,
        'Z': 3,
    }

    CONVERT = {
        'A': 'X',
        'B': 'Y',
        'C': 'Z',
        'X': 'A',
        'Y': 'B',
        'Z': 'C',
    }

    WINNING_HANDS = {
        'A': 'Y',
        'B': 'Z',
        'C': 'X'
    }

    def rock_paper_scissors(self, other_hand: str, my_hand: str, recursed: bool = False):
        """
        Play rock paper scissors

        :param other_hand: A, B, C for rock, paper, scissors
        :param my_hand: X, Y, Z for rock, paper, scissors
        :param recursed: Only recurse this function once
        :return: 1 if I win, -1 if I lose, 0 for a draw
        """
        # Check if my_hand has won
        if my_hand == self.WINNING_HANDS[other_hand]:
            return 1
        # Check if the other hand wins
        if recursed is False\
                and self.rock_paper_scissors(self.CONVERT[my_hand], self.CONVERT[other_hand], True) == 1:
            return -1
        # Draw
        return 0

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        score = 0
        for game_round in data:
            score += self.SHAPE_SCORE[game_round[1]]
            score += self.rock_paper_scissors(game_round[0], game_round[1]) * 3 + 3
        return score

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        score = 0
        for game_round in data:
            game_round[1] = self.determine_hand(game_round)
            score += self.SHAPE_SCORE[game_round[1]]
            score += self.rock_paper_scissors(game_round[0], game_round[1]) * 3 + 3
        return score

    def determine_hand(self, game_round):
        if game_round[1] == 'Y':
            return self.CONVERT[game_round[0]]
        if game_round[1] == 'Z':
            return self.WINNING_HANDS[game_round[0]]
        return self.WINNING_HANDS[self.CONVERT[self.WINNING_HANDS[game_round[0]]]]


if __name__ == "__main__":
    # Load task
    t = Task2()

    # Run task
    t.run_all()
