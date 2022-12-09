from utils.decorators import timer, debug
from utils.task import Task


class Task9(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 9

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        head = [0, 0]
        tail = [0, 0]
        seen = {(0, 0)}
        for move in data:
            for _ in range(int(move[1])):
                head = self.move_head(head=head, true_move=move[0])
                tail = self.move_rope(head, tail)
                seen.add((tail[0], tail[1]))
        return len(seen)

    @staticmethod
    def move_head(head, true_move):
        # Move the first head
        match true_move:
            case "R":
                head[0] += 1
            case "L":
                head[0] -= 1
            case "U":
                head[1] += 1
            case "D":
                head[1] -= 1
        return head

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        knots = {i: [0, 0] for i in range(10)}
        seen = {(0, 0)}
        for i, true_move in enumerate(data):
            for _ in range(int(true_move[1])):
                # Move the head
                knots[0] = self.move_head(knots[0], true_move[0])
                # Chain the other knots
                for knot in range(9):
                    new_position = self.move_rope(knots[knot], knots[knot + 1])
                    knots[knot + 1] = new_position
                seen.add((knots[9][0], knots[9][1]))
        return len(seen)

    @staticmethod
    def move_rope(head: list, tail: list):
        horizontal, vertical = None, None
        moved = False
        # Move tail right one
        if head[0] > tail[0] + 1:
            horizontal = head[0] - 1
            moved = True
        # Move tail left one
        if head[0] < tail[0] - 1:
            horizontal = head[0] + 1
            moved = True
        # Move tail up one
        if head[1] > tail[1] + 1:
            vertical = head[1] - 1
            moved = True
        # Move tail down one
        if head[1] < tail[1] - 1:
            vertical = head[1] + 1
            moved = True
        if not moved:
            return tail
        horizontal = head[0] if horizontal is None else horizontal
        vertical = head[1] if vertical is None else vertical
        return [horizontal, vertical]


if __name__ == "__main__":
    # Load task
    t = Task9()

    # Run task
    t.run_all()
