from utils.decorators import timer, debug_shape
from utils.task import Task
import numpy as np


class Task20(Task):
    # Task constants
    YEAR = 2021
    TASK_NUM = 20

    def preprocess(self, data: list) -> list:
        """
        Convert light pixels '#' to 1's and dark pixels '.' to 0's, also swap the position of the algorithm and grid

        :param data: List with image enhancement algorithm and initial input image
        :return: List with two elements, [1] a 2D numpy array with the image, [2] image enhancement algorithm
        """
        enhancement = np.array([0 if char == "." else 1 for char in data[0]])
        grid = np.array([np.array([0 if char == "." else 1 for char in row]) for row in data[2:]])
        return [grid, enhancement]

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list, num_steps: int = 2) -> int:
        """
        Determine the number of lit pixels in the image after ```num_steps``` image augmentation steps

        :param data: List with two elements, [1] a 2D numpy array with the image, [2] image enhancement algorithm
        :param num_steps: Amount of image augmentation steps to run (part 1 = 2, part 2 = 50)
        :return: Number of lit pixels in the image
        """
        grid = data[0]
        enhancement = data[1]
        for step in range(num_steps):
            grid = self.augment_image(grid, enhancement, step)
        return int(sum(sum(grid)))

    def augment_image(self, grid, enhancement, step: int):
        """
        Performs one step of the image enhancing algorithm on the given grid

        :param grid: The input image
        :param enhancement: The image enhancement algorithm
        :param step: The current step number
        :return: Augmented image
        """
        # The edge is full of zeros on even steps, ones on even
        if step % 2 == 0 or enhancement[0] == 0:
            new_grid = np.zeros((grid.shape[0] + 2, grid.shape[1] + 2))
        else:
            new_grid = np.ones((grid.shape[0] + 2, grid.shape[1] + 2))
        new_grid[1:-1, 1:-1] = grid
        # Augment each pixel individually
        modified_grid = np.zeros((grid.shape[0] + 2, grid.shape[1] + 2))
        for i in range(new_grid.shape[0]):
            for j in range(new_grid.shape[1]):
                # Augment pixel
                index = self.find_enhancement_index(new_grid[max(i - 1, 0):i + 2, max(j - 1, 0):j + 2],
                                                    i, j, step, enhancement)
                modified_grid[i, j] = enhancement[index]
        return modified_grid

    def find_enhancement_index(self, square: np.ndarray, i: int, j: int, step: int, enhancement: list) -> int:
        """
        Determine the index of this slice for the image enhancement algorithm

        :param square: The input slice to pad to a 3x3 square
        :param i: The y position of the center of the slice in the image
        :param j: The x position of the center of the slice in the image
        :param step: The current image enhancement step
        :param enhancement: The image enhancement algorithm
        :return:
        """
        # Literal edge cases, pad the sides with the correct digit (odd 0, even 1)
        if square.shape != (3, 3):
            y = 1 if i == 0 else 0
            x = 1 if j == 0 else 0
            square = self.pad_edges(square, y, x, step, enhancement)
        # Take a 3x3 square slice of the grid, create a binary number from the 9 values, convert to decimal
        return int("".join([str(0) if val == 0 else str(1) for row in square for val in row]), 2)

    @staticmethod
    def pad_edges(square: np.ndarray, place_y: int, place_x: int, step: int, enhancement: list) -> np.ndarray:
        """
        Pad the input slice to a 3x3 square
        The side(s) to pad on depends on the given place_y and place_x where the top-left coordinate is meant to be
        Padding is done with 0's or 1's, 0 is the default case, 1's are used on odd steps when enhancement[0] == 1

        :param square: The input slice to pad to a 3x3 square
        :param place_y: The y position of the top-left point in the padded square
        :param place_x: The x position of the top-left point in the padded square
        :param step: The current image enhancement step
        :param enhancement: The image enhancement algorithm
        :return: A 3x3 padded square
        """
        if step % 2 == 0 or enhancement[0] == 0:
            grid = np.zeros((3, 3))
        else:
            grid = np.ones((3, 3))
        grid[place_y:place_y + square.shape[0], place_x:place_x + square.shape[1]] = square
        return grid

    @debug_shape
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        """
        Determine the number of lit pixels in the image after 50 image augmentation steps
        Use the implementation of part 1

        :param data: List with two elements, [1] a 2D numpy array with the image, [2] image enhancement algorithm
        :return: Number of lit pixels in the image
        """
        return self.part_1(data, 50)


if __name__ == "__main__":
    # Load task
    t = Task20()

    # Run task
    t.run_all()
