from utils.decorators import timer, debug
from utils.task import Task


class Task13(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 13

    def preprocess(self, data: list) -> dict:
        """
        Split input data into dots and fold commands
         Dots are coordinates in a grid (x, y)
         Folds are a string 'x' or 'y' followed by an integer indicating the line to fold from

        :param data: List of dots and fold commands, separated by an empty list index ''
        :return: Dictionary with 'dots' and 'folds' as key, both are lists with associated objects
        """
        out_data = {'dots': [], 'folds': []}
        # Find the split between dots and folds
        split = data.index('')
        dots = data[:split]
        folds = data[split+1:]
        # Format all dots into [x, y]
        for dot in dots:
            value1, value2 = dot.split(',')
            out_data['dots'].append([int(value1), int(value2)])
        # Format all fold commands into ('x', value) or ('y', value)
        for fold in folds:
            value1, value2 = fold[2].split('=')
            out_data['folds'].append((value1, int(value2)))
        return out_data

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: dict) -> int:
        """
        Fold the paper once and count the amount of visible dots

        :param data: Dictionary with dots and folds
        :return: Number of visible dots
        """
        for fold in data['folds']:
            data = self.fold_paper(data, fold)
            break
        return len(data['dots'])

    def fold_paper(self, data, fold):
        to_remove = []
        fold_value = fold[1]
        fold_direction = 0 if fold[0] == 'x' else 1
        # Check which dots are on the folding side and change their coordinates
        for i, dot in enumerate(data['dots']):
            if dot[fold_direction] > fold_value:
                new_dot = self.fold_dot(dot, fold_direction, fold_value)
                # Overlapping dots are merged into one (one of them is removed)
                if new_dot in data['dots']:
                    to_remove.append(dot)
                else:
                    data['dots'][i] = new_dot
        # Remove all duplicate dots
        for dot in to_remove:
            data['dots'].remove(dot)
        return data

    @staticmethod
    def fold_dot(dot, fold_direction, fold_value):
        new_dot = dot.copy()
        if -2 * (dot[fold_direction] - fold_value) + dot[fold_direction] != 2 * fold_value - dot[fold_direction]:
            raise ValueError("Error")
        new_value = 2 * fold_value - dot[fold_direction]
        new_dot[fold_direction] = new_value
        return new_dot

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: dict) -> int:
        """
        Fold the paper with dots and reveal the final 8 capital letters

        :param data: Dictionary with dots and folds
        :return: Nothing important
        """
        for fold in data['folds']:
            data = self.fold_paper(data, fold)
        # Setup the grid with dots
        grid = [["\033[0;33m.\033[0m" for _ in range(8*5)] for _ in range(6)]
        for dot in data['dots']:
            grid[dot[1]][dot[0]] = "#"
        # Print the grid
        for row in grid:
            print("".join(row))
        return 0


if __name__ == "__main__":
    # Load task
    t = Task13()

    # Run task
    t.run_all()
