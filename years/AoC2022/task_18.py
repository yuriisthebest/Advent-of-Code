from utils.decorators import timer, debug
from utils.task import Task


class Task18(Task):
    # Task constants
    YEAR = 2022
    TASK_NUM = 18

    def preprocess(self, data: list) -> list:
        return [[int(num) for num in line.split(",")] for line in data]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        # Calculate the surface area of the droplet
        surface_area = 0
        for cube in data:
            surface_area += 6
            for direction in [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]:
                adjacent_cube = [cube_coord + adjacent for cube_coord, adjacent in zip(cube, direction)]
                if adjacent_cube in data:
                    surface_area -= 1
        return surface_area

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> int:
        # Calculate the surface area of the droplet
        surface_area = 0
        air_cubes = []
        for cube in data:
            surface_area += 6
            for direction in [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]:
                adjacent_cube = [cube_coord + adjacent for cube_coord, adjacent in zip(cube, direction)]
                if adjacent_cube in data:
                    surface_area -= 1
                else:
                    air_cubes.append(adjacent_cube)
        # Extreme values
        largest_coord = max([max(cube) for cube in data]) + 1
        target = [largest_coord, largest_coord, largest_coord]
        # Find enclosed air bubbles
        seen_enclosures = []
        for air_cube in air_cubes:
            # If the cube is known to be enclosed, we can stop trying to get out
            if air_cube in seen_enclosures:
                surface_area -= 1
                continue
            # Use a pathfinder to try and reach an extreme value
            seen = [air_cube]
            todo = [(air_cube, self.manhattan_distance(air_cube, target))]
            reached_target = False
            while len(todo) != 0:
                cube, heuristic = todo.pop(0)
                # Add the neighbors
                for direction in [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]:
                    adjacent_cube = [cube_coord + adjacent for cube_coord, adjacent in zip(cube, direction)]
                    if adjacent_cube == target:
                        reached_target = True
                        break
                    if adjacent_cube in seen or adjacent_cube in data:
                        continue
                    todo.append((adjacent_cube, self.manhattan_distance(adjacent_cube, target)))
                    todo.sort(key=lambda x: x[1])
                    seen.append(adjacent_cube)
                if adjacent_cube == target:
                    reached_target = True
                    break
            # The current air_cube is enclosed
            if not reached_target:
                seen_enclosures.extend(seen)
                surface_area -= 1
        return surface_area

    @staticmethod
    def manhattan_distance(cube1, cube2):
        """
        Calculate the manhattan distance

        :param cube1: 3d coordinates representing a cube
        :param cube2: 3d coordinates representing a cube
        :return: The manhattan distance of the cubes
        """
        return sum([abs(cube1[i] - cube2[i]) for i in range(3)])


if __name__ == "__main__":
    # Load task
    t = Task18()

    # Run task
    t.run_all()
