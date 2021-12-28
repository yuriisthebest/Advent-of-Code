from utils.decorators import timer, debug
from utils.task import Task


quantum_dice = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}


class Dice:
    def __init__(self, max_roll: int):
        self.rolls = 0
        self.__die = self.__deterministic_dice(max_roll)

    def roll(self):
        self.rolls += 1
        return next(self.__die)

    @staticmethod
    def __deterministic_dice(max_roll: int):
        while True:
            for i in range(max_roll):
                yield i + 1


class Player:
    def __init__(self, name: str, starting_pos: int, winning_score: int, starting_score: int = 0):
        self.name = name
        self.position = starting_pos
        self.winning_score = winning_score
        self.score = starting_score

    def __repr__(self):
        return f"player {self.name} on position {self.position} with {self.score} points"

    def __eq__(self, other):
        return self.name == other.name and self.position == other.position and self.score == other.score

    def __hash__(self):
        return hash((self.position, self.score))

    @staticmethod
    def advance(starting_position: int, spaces: int) -> int:
        """
        Advances the player x amount of spaces, looping back at 1 after 10

        :param starting_position: The starting position
        :param spaces: The amount of spaces to move forward
        :return: New position
        """
        position = spaces + starting_position
        position %= 10
        if position == 0:
            position = 10
        return position

    def turn(self, die: Dice) -> bool:
        """
        Perform one normal turn

        :param die: The dice to throw
        :return: Boolean indicating if the player has won
        """
        # Roll the die 3 times
        roll = sum([die.roll() for _ in range(3)])
        self.position = self.advance(self.position, roll)
        self.score += self.position
        return self.score >= 1000

    def quantum_turn(self, positions: dict) -> dict:
        new_positions = {}
        for game in positions:
            # Don't take a turn if the game is over
            if game.is_over():
                if game not in new_positions:
                    new_positions[game] = 0
                new_positions[game] += positions[game]
                continue
            # Take a turn for 1 player
            for roll in quantum_dice:
                player, other = game.get_player_from_name(self.name)
                new_space = self.advance(player.position, roll)
                new_player = Player(player.name, new_space, 21, player.score + new_space)
                new_game = Game(new_player, other) if player.name == '1' else Game(other, new_player)
                if new_game not in new_positions:
                    new_positions[new_game] = 0
                new_positions[new_game] += quantum_dice[roll] * positions[game]
        return new_positions


class Game:
    def __init__(self, p1: Player, p2: Player):
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, other: 'Game'):
        return (self.p1.position == other.p1.position
                and self.p1.score == other.p1.score
                and self.p2.position == other.p2.position
                and self.p2.score == other.p2.score)

    def __hash__(self):
        return hash((self.p1.score, self.p1.position, self.p2.score, self.p2.position))

    def __repr__(self):
        return f"Game ({self.p1.score} <{self.p1.position}>, {self.p2.score} <{self.p2.position}>)"

    def is_over(self) -> bool:
        if self.p1.score >= 21:
            return True
        if self.p2.score >= 21:
            return True
        return False

    def get_player_from_name(self, name: str):
        if name == self.p1.name:
            return self.p1, self.p2
        if name == self.p2.name:
            return self.p2, self.p1


class Task21(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 21

    def preprocess(self, data: list) -> list:
        """
        Extract the name and starting position of both players

        :param data: Nested lists where each list contains the name and starting position of the player
        :return: List of Players
        """
        output = []
        for participant in data:
            player = Player(participant[1], int(participant[4]), 1000)
            output.append(player)
        return output

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        """
        Play a single game of Dirac Dice with a deterministic dice

        :param data: List of Players
        :return: The product of the points of the loser and the amount of times the dice was thrown
        """
        die = Dice(100)
        player1: Player = data[0]
        player2: Player = data[1]
        loser_points = self.play_game(die, player1, player2)
        return loser_points * die.rolls

    @staticmethod
    def play_game(die, player1, player2):
        # Keep playing until one player wins
        while True:
            if player1.turn(die):
                loser_points = player2.score
                break
            if player2.turn(die):
                loser_points = player1.score
                break
        return loser_points

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Play a game of Dirac Dice and find who

        :param data: List of players
        :return: The amount of times the winner won Dirac Dice
        """
        win_score = 21
        player1: Player = data[0]
        player1.winning_score = win_score
        player2: Player = data[1]
        player2.winning_score = win_score
        game = Game(player1, player2)
        positions = {game: 1}
        # Play the game until all games have finished
        while self.still_playing(positions):
            positions = player1.quantum_turn(positions)
            positions = player2.quantum_turn(positions)

        # Determine winner
        p1_wins = sum([positions[game] for game in positions if game.p1.score >= win_score])
        p2_wins = sum([positions[game] for game in positions if game.p2.score >= win_score])
        return p1_wins if p1_wins > p2_wins else p2_wins

    @staticmethod
    def still_playing(positions: dict):
        """
        Return true if at least 1 game is still playing
        """
        for game in positions:
            if not game.is_over():
                return True
        return False


if __name__ == "__main__":
    # Load task
    t = Task21()

    # Run task
    t.run_all()
