from utils.decorators import timer, debug
from utils.task import Task


def check_cards(card: list, numbers: list) -> bool:
    # Check rows
    for row in card:
        for value in row:
            if value not in numbers:
                break
        else:
            # The row if full, winner!
            return True
    # Check columns
    for i in range(5):
        for j in range(5):
            if card[j][i] not in numbers:
                break
        else:
            # The column if full, winner!
            return True
    return False


def calculate_score(card: list, numbers: list) -> int:
    return sum([value for row in card for value in row if value not in numbers])


class Task4(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 4

    def preprocess(self, data: list):
        bingo_numbers = [int(num) for num in data[0].split(",")]
        cards = []
        i = 2
        while i < len(data):
            card = data[i:i + 5]
            card = [[int(value) for value in row if value != ''] for row in card]
            cards.append(card)
            i += 6
        return bingo_numbers, cards

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: tuple) -> int:
        """
        Play bingo and identify which card wins first
        Calculate a score based on the winning card and number

        :param data: Tuple of two lists, first list contains the bingo numbers, second list contains bingo cards
        :return: A score based on the winning card and number, solution to advent of code AoC2021 task 4 part 1
        """
        bingo, cards = data
        for i, num in enumerate(bingo):
            for card in cards:
                if check_cards(card, bingo[:i + 1]):
                    # This card won, calculate score
                    return calculate_score(card, bingo[:i + 1]) * num

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: tuple) -> int:
        """
        Play bingo and identify which card wins last
        Calculate a score based on the winning card and number

        :param data: Tuple of two lists, first list contains the bingo numbers, second list contains bingo cards
        :return: A score based on the winning card and number, solution to advent of code AoC2021 task 4 part 2
        """
        bingo, cards = data
        complete_cards = {i: False for i in range(len(cards))}
        complete_count = 0
        for i, num in enumerate(bingo):
            for j, card in enumerate(cards):
                if check_cards(card, bingo[:i + 1]):
                    # This card won, add it to the completes
                    if not complete_cards[j]:
                        complete_cards[j] = True
                        complete_count += 1
                    # This was the final card to win, calculate score
                    if complete_count == len(cards):
                        return calculate_score(card, bingo[:i + 1]) * num


if __name__ == "__main__":
    # Load task
    t = Task4()

    # Run task
    t.run_all()
