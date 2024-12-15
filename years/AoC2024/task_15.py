from utils.decorators import timer, debug
from utils.task import Task


class Task15(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 15
    # TEST_MODE = True

    DIRECTION = {
        "<": (0, -1),
        ">": (0, 1),
        "^": (-1, 0),
        "v": (1, 0),
    }

    def preprocess(self, data: list) -> tuple:
        warehouse = []
        read_warehouse = True
        moves = []
        for line in data:
            if line == "":
                read_warehouse = False
            if read_warehouse:
                warehouse.append([char for char in line])
            else:
                moves.append(line)
        moves = "".join(moves)
        return warehouse, moves

    @staticmethod
    def find_bot(warehouse: list) -> tuple:
        for i, row in enumerate(warehouse):
            for j, char in enumerate(row):
                if char == "@":
                    return i, j

    def make_move(self, warehouse: list, move: chr, i: int, j: int):
        direction = self.DIRECTION[move]
        if warehouse[i + direction[0]][j + direction[1]] == "#":
            return False
        elif warehouse[i + direction[0]][j + direction[1]] == ".":
            warehouse[i + direction[0]][j + direction[1]] = warehouse[i][j]
            warehouse[i][j] = "."
            return True
        else:
            if self.make_move(warehouse, move, i + direction[0], j + direction[1]):
                warehouse[i + direction[0]][j + direction[1]] = warehouse[i][j]
                warehouse[i][j] = "."
                return True

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        warehouse, moves = data
        for move in moves:
            bot_pos = self.find_bot(warehouse)
            self.make_move(warehouse, move, *bot_pos)
        # Find all boxes
        gps = 0
        for i, line in enumerate(warehouse):
            for j, char in enumerate(line):
                if char == "O":
                    gps += i * 100 + j
        return gps

    def make_move2(self, warehouse: list, move: chr, i: int, j: int, advanced: bool = False):
        direction = self.DIRECTION[move]
        if warehouse[i + direction[0]][j + direction[1]] == "#":
            # Found a wall, cannot move
            return []
        elif warehouse[i + direction[0]][j + direction[1]] == ".":
            # Found a free space, this can move
            return [(i, j, warehouse[i][j])]
        elif direction[0] == 0 or not advanced:
            # Check if next space is free, if so then move
            next_moves = self.make_move2(warehouse, move, i + direction[0], j + direction[1], advanced)
            if len(next_moves) == 0:
                return []
            next_moves.append((i, j, warehouse[i][j]))
            return next_moves
        elif warehouse[i + direction[0]][j + direction[1]] == "[":
            moves_left = self.make_move2(warehouse, move, i + direction[0], j + direction[1], advanced)
            moves_right = self.make_move2(warehouse, move, i + direction[0], j + direction[1] + 1, advanced)
            if len(moves_left) == 0 or len(moves_right) == 0:
                return []
            moves = []
            moves.extend(moves_left)
            for m in moves_right:
                if m not in moves:
                    moves.append(m)
            moves.append((i, j, warehouse[i][j]))
            return moves
        elif warehouse[i + direction[0]][j + direction[1]] == "]":
            moves_left = self.make_move2(warehouse, move, i + direction[0], j + direction[1] - 1, advanced)
            moves_right = self.make_move2(warehouse, move, i + direction[0], j + direction[1], advanced)
            if len(moves_left) == 0 or len(moves_right) == 0:
                return []
            moves = []
            moves.extend(moves_left)
            for m in moves_right:
                if m not in moves:
                    moves.append(m)
            moves.append((i, j, warehouse[i][j]))
            return moves
        else:
            print("HOW?")

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        warehouse, moves = data
        warehouse = self.modify_warehouse(warehouse)
        # Process moves
        for move in moves:
            bot_pos = self.find_bot(warehouse)
            sceduled_moves = self.make_move2(warehouse, move, *bot_pos, True)
            for new_move in sceduled_moves:
                direction = self.DIRECTION[move]
                warehouse[new_move[0] + direction[0]][new_move[1] + direction[1]] = new_move[2]
                warehouse[new_move[0]][new_move[1]] = "."
        # Find all boxes
        gps = 0
        for i, line in enumerate(warehouse):
            for j, char in enumerate(line):
                if char == "[":
                    gps += i * 100 + j
        return gps

    @staticmethod
    def modify_warehouse(warehouse):
        # Create new warehouse
        new_warehouse = []
        for line in warehouse:
            new_line = []
            for char in line:
                if char == "#" or char == ".":
                    new_line.append(char)
                    new_line.append(char)
                elif char == "O":
                    new_line.append("[")
                    new_line.append("]")
                elif char == "@":
                    new_line.append(char)
                    new_line.append(".")
            new_warehouse.append(new_line)
        warehouse = new_warehouse
        return warehouse

    @staticmethod
    def print_warehouse(warehouse: list):
        for i, line in enumerate(warehouse):
            print("".join(line))


if __name__ == "__main__":
    # Load task
    t = Task15()

    # Run task
    t.run_all()
