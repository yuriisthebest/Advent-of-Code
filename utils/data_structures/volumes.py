from __future__ import annotations
from itertools import product

from utils.data_structures.tags import Tags


class Volume(Tags):
    """N-Dimensional object"""
    def __init__(self, coord1: tuple, coord2: tuple):
        """
        N-Dimensional object with straight edges and faces;
        Coords are inclusive

        :param coord1: N-dimensional coordinate
        :param coord2: Second N-dimensional coordinate with different values from the first coordinate
        """
        if len(coord1) != len(coord2):
            raise ValueError(f"Dimensions do not match: {len(coord1)} != {len(coord2)}")
        super().__init__()
        self.__minimums = [min(dim_value1, dim_value2) for dim_value1, dim_value2 in zip(coord1, coord2)]
        self.__maximums = [max(dim_value1, dim_value2) for dim_value1, dim_value2 in zip(coord1, coord2)]

    def __repr__(self) -> str:
        return f"<Volume of size {self.size} with coords: {self.__minimums}; {self.__maximums}>"

    @property
    def size(self) -> int:
        size = 1
        for dim_size in self.dims:
            size *= dim_size
        return size

    @property
    def dims(self) -> tuple:
        return tuple(large - small + 1 for large, small in zip(self.__maximums, self.__minimums))

    @property
    def corners(self) -> list[tuple]:
        corners = []
        for settings in product([0, 1], repeat=len(self.dims)):
            point = []
            for dim in range(len(self.dims)):
                point.append(self.__minimums[dim] if settings[dim] == 0 else self.__maximums[dim])
            corners.append(tuple(point))
        return corners

    def overlaps(self, other: Volume) -> bool:
        # TODO
        pass

    def intersects(self, other: Volume) -> bool:
        """
        Whether two volumes in 2D-space
        # TODO: generalize
        # TODO: implement
        # TODO: add explanation about why intersecting and overlapping are two different things

        :param other: Another Volume
        :return: True if the two volumes intersect each other
        """
        # # The two volumes must have overlap on each dimension
        # if self.__minimums[0] > other.__maximums[0]:
        #     return False
        # if self.__minimums[1] > other.__maximums[1]:
        #     return False
        # if self.__maximums[0] < other.__minimums[0]:
        #     return False
        # if self.__maximums[1] < other.__minimums[1]:
        #     return False
        # # There is some overlap,
        # # if we find a dimension where one min and max are smaller and greater than the other min and max,
        # # it has been intersected
        # if self.__minimums[0] < other.__minimums[0] and self.__maximums[0] > other.__maximums[0]:
        #     print("CASE A")
        #     return True
        # if other.__minimums[0] < self.__minimums[0] and other.__maximums[0] > self.__maximums[0]:
        #     print("CASE B")
        #     return True
        # if self.__minimums[1] < other.__minimums[1] and self.__maximums[1] > other.__maximums[1]:
        #     print("CASE C")
        #     return True
        # if other.__minimums[1] < self.__minimums[1] and other.__maximums[1] > self.__maximums[1]:
        #     print("CASE D")
        #     return True
        # # No intersection found
        # return False

    def contains(self, point: tuple) -> bool:
        if len(point) != len(self.__maximums):
            raise ValueError(f"Dimensions do not match: {len(point)}")
        for dim, value in enumerate(point):
            if self.__minimums[dim] > value or value > self.__maximums[dim]:
                return False
        return True

    def on_edge(self, point: tuple):
        # Point must be in volume
        if not self.contains(point):
            return False
        # Check if on the edge
        for dim, value in enumerate(point):
            if value == self.__minimums[dim] or value == self.__maximums[dim]:
                return True
        return False

    def get_edge_values(self):
        # First find the corners of the volume
        corners = self.corners
        # Find all points
        edge_points = set()
        for i, corner1 in enumerate(corners):
            for corner2 in corners[i:]:
                dim_changes = [dim_value1-dim_value2 for dim_value1, dim_value2 in zip(corner1, corner2)]
                if dim_changes.count(0) != len(self.dims) - 1:
                    continue
                variable_dim = None
                for dim, change in enumerate(dim_changes):
                    if change != 0:
                        variable_dim = dim
                for edge_point in range(min([corner1[variable_dim], corner2[variable_dim]]),
                                        max([corner1[variable_dim], corner2[variable_dim]]) + 1):
                    new_point = list(corner1)
                    new_point[variable_dim] = edge_point
                    edge_points.add(tuple(new_point))
        return edge_points


if __name__ == "__main__":
    bar = Volume((0, 0, 0), (3, 3, 3))
    print(f"bar dims: {bar.dims}")
    points = [(1, 2, 3), (0, 0, 1), (3, 3, 3), (-1, 0, 0), (-2, 1, 1), (1, 5, -2), (2, 2, 2), (2, 5, 2)]
    for p in points:
        print(f"Bar {bar} contains point {p} == {bar.contains(p)}; On Edge: {bar.on_edge(p)}")
