class GridPoint:
    def __init__(self, value=None, neighbors: list = None, tags: dict = None):
        """
        A GridPoint can have a value or any type, a list of neighbors and some tags
        """
        if tags is None:
            tags = {}
        self.__value = value
        self.__neighbors = neighbors
        self.tags = tags

    @property
    def value(self):
        """
        The value of a GridPoint can be anything.
        """
        return self.__value

    @set
    def value(self, new_value):
        """
        The value of a GridPoint can be anything.
        """
        self.__value = new_value

    def get_neighbors(self, inclusive: list, exclusive: list) -> list:
        """
        Return the neighbors of the GridPoint

        If a list of inclusive values is given, only those neighbors with an included value are returned.
        If a list of exclusive values is given, only those neighbors with a different value are returned.
        Inclusiveness has precedence over exclusiveness (so don't supply inclusive in an exclusive search).

        :param inclusive: A list of allowed values for neighbors to have
        :param exclusive: A list of disallowed values that neighbors may not have to be considered neighbors
        :return: The neighbors of this GridPoint, conditioned on the inclusive or exclusive properties
        """
        if len(inclusive) > 0:
            return [neighbor for neighbor in self.__neighbors
                    if neighbor.value in inclusive]
        return [neighbor for neighbor in self.__neighbors
                if neighbor.value not in exclusive]

    def add_neighbor(self, other) -> None:
        """
        Identify two GridPoints as neighbors.
        Update both to reflect their neighboring status.
        """
        self.__neighbors.append(other)
        other.__neighbors.append(self)


class Grid2D:
    def __init__(self, grid: list):
        self.grid = None
        self.load_grid(grid)

    def load_grid(self, grid: list) -> None:
        """
        Destructively load a 2d-grid from a list of lists.
        """
        new_grid = []
        for i, row in enumerate(grid):
            new_row = []
            for j, val in enumerate(row):
                point = GridPoint(value=val)
                # Add neighbors
                if j > 0:
                    point.add_neighbor(new_row[-1])
                if i > 0:
                    point.add_neighbor(new_grid[i - 1][j])
                # Add new GridPoint to Grid
                new_row.append(point)
        self.grid = new_grid
