from utils.decorators import timer, debug
from utils.task import Task


class Task7(Task):
    # Task constants
    YEAR = 2023
    TASK_NUM = 7

    LABELS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    LABELS2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        weak_to_strong_hands = []
        for hand, bet in data:
            type1 = self.get_type(hand, self.LABELS, False)
            for i, (contender, bet2) in enumerate(weak_to_strong_hands):
                # If the hand is weaker than the contender, the hand should be in front of the contender
                if self.is_weaker(hand, type1, contender, self.LABELS, False):
                    weak_to_strong_hands.insert(i, (hand, bet))
                    break
            # If the hand is stronger than all contenders, add it to the end
            else:
                weak_to_strong_hands.append((hand, bet))
        return sum([int(bet) * (i + 1) for i, (_, bet) in enumerate(weak_to_strong_hands)])

    def is_weaker(self, hand1: str, type1: int, hand2: str, labels: list, jokers: bool) -> bool:
        type2 = self.get_type(hand2, labels, jokers)
        # If the types do not match, return whether hand 1 is weaker
        if type1 != type2:
            return type1 < type2
        # Type is equal, find first higher card
        for char1, char2 in zip(hand1, hand2):
            card1 = labels.index(char1)
            card2 = labels.index(char2)
            if card1 == card2:
                continue
            return card1 > card2

    @staticmethod
    def get_type(hand: str, labels: list, jokers: bool) -> int:
        """
        Return and integer representing the type of the hand
        five of a kind = 6
        four of a kind = 5
        full house = 4
        three of a kind = 3
        two pair = 2
        one pair = 1
        high card = 0

        :param labels: The ordered list of cards
        :param jokers: Whether to use jokers
        :param hand: String representing a hand in Camel Cards
        :return: Integer representing type of hand
        """
        counts = []
        num_jokers = 0
        if jokers:
            num_jokers = hand.count("J")
            labels = labels[:-1]
        for label in labels:
            c = hand.count(label)
            # Five of a kind
            if c + num_jokers == 5 or num_jokers == 4:
                return 6
            # Four of a kind
            if c + num_jokers == 4:
                return 5
            if c > 1:
                counts.append(c)
        # Full house
        if (3 in counts and 2 in counts) or (num_jokers == 1 and len(counts) == 2):
            return 4
        # Three of a kind
        if 3 in counts or num_jokers == 2 or (num_jokers == 1 and 2 in counts):
            return 3
        # Two pair
        if len(counts) == 2:
            return 2
        # One pair
        if 2 in counts or num_jokers == 1:
            return 1
        return 0

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        weak_to_strong_hands = []
        for hand, bet in data:
            type1 = self.get_type(hand, self.LABELS2, True)
            for i, (contender, bet2) in enumerate(weak_to_strong_hands):
                # If the hand is weaker than the contender, the hand should be in front of the contender
                if self.is_weaker(hand, type1, contender, self.LABELS2, True):
                    weak_to_strong_hands.insert(i, (hand, bet))
                    break
            # If the hand is stronger than all contenders, add it to the end
            else:
                weak_to_strong_hands.append((hand, bet))
        return sum([int(bet) * (i + 1) for i, (_, bet) in enumerate(weak_to_strong_hands)])


if __name__ == "__main__":
    # Load task
    t = Task7()

    # Run task
    t.run_all()
