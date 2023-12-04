from utils.decorators import timer, debug
from utils.task import Task


class Task4(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 4

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        result = 0
        for line in data:
            total_wins = self.count_wins(line)
            # Determine score of scratchcard (0 wins = 0 points)
            if total_wins > 0:
                result += 2**(total_wins - 1)
        return result

    @staticmethod
    def count_wins(line):
        """
        Determine how many wins a single scratchcard has

        :param line: Scratchcard
        :return: Number of wins
        """
        winning_numbers = []
        numbers = []
        read_winning = True
        for element in line:
            # Switch from reading winning numbers to card numbers
            if element == "|":
                read_winning = False
            # Read a number
            elif element.isnumeric():
                if read_winning:
                    winning_numbers.append(int(element))
                else:
                    numbers.append(int(element))
        # Count how many numbers are winning numbers
        total_wins = 0
        for num in numbers:
            if num in winning_numbers:
                total_wins += 1
        return total_wins

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        cards = {i: 1 for i in range(len(data))}
        for card_id, line in enumerate(data):
            total_wins = self.count_wins(line)
            # Maintain number of copies of each scratchcard
            for i in range(total_wins):
                cards[card_id + i + 1] += cards[card_id]
        return sum(cards.values())


if __name__ == "__main__":
    # Load task
    t = Task4()

    # Run task
    t.run_all()
