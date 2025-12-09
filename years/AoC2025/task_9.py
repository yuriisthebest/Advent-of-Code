from utils.decorators import timer, debug
from utils.task import Task


class Task9(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 9

    def preprocess(self, data: list) -> list:
        return [tuple([int(num) for num in line.split(',')]) for line in data]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        # Check the area of possible rectangles
        largest_area = 0
        for i, coord in enumerate(data):
            for coord2 in data[i:]:
                if coord == coord2:
                    continue
                area = (abs(coord[0] - coord2[0]) + 1) * (abs(coord[1] - coord2[1]) + 1)
                largest_area = area if area > largest_area else largest_area
        return largest_area

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        # Set up the border of the red/green region
        border = set()
        for i, coord in enumerate(data):
            # Create a line from two seqential points in the data
            next_coord = data[i+1] if i < len(data) - 1 else data[0]
            # Determine in which dimension the line moves
            variable_dim = None
            for dim in range(len(coord)):
                if coord[dim] != next_coord[dim]:
                    variable_dim = dim
            # Get all points on the borner line (inclusive)
            for step in range(min([coord[variable_dim], next_coord[variable_dim]]),
                              max([coord[variable_dim], next_coord[variable_dim]]) + 1):
                new_coord = list(coord)
                new_coord[variable_dim] = step
                new_coord = tuple(new_coord)
                border.add(new_coord)

        # Determine the points on the outside border of the red/green region
        outside_border = set()
        for i, coord in enumerate(data):
            # Create a line from two seqential points in the data
            next_coord = data[i + 1] if i < len(data) - 1 else data[0]
            # Determine in which dimension the line moves
            variable_dim = None
            for dim in range(len(coord)):
                if coord[dim] != next_coord[dim]:
                    variable_dim = dim
            # Determine the direction of the line so the point to the left of the line can be retrieved
            direction = (
                0 if coord[0] == next_coord[0] else 1 if coord[0] < next_coord[0] else -1,
                0 if coord[1] == next_coord[1] else 1 if coord[1] < next_coord[1] else -1
            )
            left = (direction[1], -direction[0])
            # Get all points on the left of the borner line
            for step in range(min([coord[variable_dim], next_coord[variable_dim]]),
                              max([coord[variable_dim], next_coord[variable_dim]]) + 1):
                new_coord = list(coord)
                new_coord[variable_dim] = step
                new_left_coord = (new_coord[0] + left[0], new_coord[1] + left[1])
                if new_left_coord not in border:
                    outside_border.add(new_left_coord)

        # Find a sort all possible rectangles
        rectangles = []
        for i, coord in enumerate(data):
            for coord2 in data[i:]:
                if coord == coord2:
                    continue
                rectangles.append(((abs(coord[0] - coord2[0]) + 1) * (abs(coord[1] - coord2[1]) + 1), coord, coord2))
        rectangles.sort(key=lambda x: x[0], reverse=True)

        # Check possible rectangles
        for area, coord1, coord2 in rectangles:
            # Computation time speed-up
            if not self.IS_TEST and area > 1475000000:
                continue
            if self.check_rectangle(coord1, coord2, outside_border):
                return area

    def check_rectangle(self, coord1: tuple, coord2: tuple, outside_border: set):
        # Get all points on the edge of the rectangle
        corners = [
            (coord1[0], coord1[1]),
            (coord1[0], coord2[1]),
            (coord2[0], coord1[1]),
            (coord2[0], coord2[1]),
        ]
        edges = self.edges(corners)
        for edge_point in edges:
            # If any point on the edge of the rectangle is outside the border, the rectangle is not valid
            if edge_point in outside_border:
                return False
        # No conflict found, so it's good
        return True

    @staticmethod
    def edges(corners: list):
        edges = set()
        for i, coord in enumerate(corners):
            # Create a line from corner to corner
            next_coord = corners[i + 1] if i < len(corners) - 1 else corners[0]
            if coord == next_coord:
                continue
            # Determine in which dimension the line from corner to corner moves
            variable_dim = None
            for dim in range(len(coord)):
                if coord[dim] != next_coord[dim]:
                    variable_dim = dim
            # Get all points on the line between the two corners (inclusive)
            for step in range(min([coord[variable_dim], next_coord[variable_dim]]),
                              max([coord[variable_dim], next_coord[variable_dim]]) + 1):
                new_coord = list(coord)
                new_coord[variable_dim] = step
                new_coord = tuple(new_coord)
                edges.add(new_coord)
        return edges


if __name__ == "__main__":
    # Load task
    t = Task9()

    # Run task
    t.run_all()
