from __future__ import annotations

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

    def has_overlap(self, other: Volume) -> bool:
        # TODO
        pass

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


if __name__ == "__main__":
    bar = Volume((0, 0, 0), (3, 3, 3))
    print(f"bar dims: {bar.dims}")
    points = [(1, 2, 3), (0, 0, 1), (3, 3, 3), (-1, 0, 0), (-2, 1, 1), (1, 5, -2), (2, 2, 2), (2, 5, 2)]
    for p in points:
        print(f"Bar {bar} contains point {p} == {bar.contains(p)}; On Edge: {bar.on_edge(p)}")
