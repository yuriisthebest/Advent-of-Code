from abc import abstractmethod

from utils.data_structures.queue import PriorityQueue


class PathFinding:
    """
    Implements basic pathfinding algorithms;
    Basic functions must be overwritten for the specific use case
    """
    def astar(self, source, target, allow: dict = None, disallow: dict = None) -> int:
        # TODO <- this might not yet be done
        """
        Implements A*

        :param source: The starting
        :param target: The ending
        :param allow: A key-value dictionary indicating a mandatory filter of tags and value-lists
        :param disallow: A key-value dictionary indicating a forbidden filter of tags and value-lists
        :return: The distance of the path, returns -1 if no path can be found
        """
        # Prepare priority queue
        sort_tag = "A*"
        todo = PriorityQueue(tag=sort_tag)
        source.update_tag({"distance": 0, sort_tag: 0, "sort_tag": sort_tag})
        todo.add(source)
        while len(todo) != 0:
            # Take the least travelled non-locked cell
            node = todo.take_first()
            node.update_tag({"locked": True})
            # Stop the search if the target has been found
            if node == target:
                return node.get("distance")
            # For each neighbor, see if it's locked, see if going there is an improvement, add it to the queue
            for neighbor in self.__get_adjacent(node, allow=allow, disallow=disallow):
                if neighbor.get("locked"):
                    continue
                distance = node.get("distance") + self.__move_cost(neighbor, node) + self.__heuristic(neighbor, target)
                if not neighbor.has_tag(sort_tag) or neighbor.get(sort_tag) < distance:
                    neighbor.update_tag({"previous": node,
                                         "distance": distance - self.__heuristic(neighbor, target),
                                         sort_tag: distance,
                                         "sort_tag": sort_tag})
                    todo.add(neighbor)
        return -1

    @abstractmethod
    def __get_adjacent(self, node, allow, disallow) -> list:
        return []

    @abstractmethod
    def __move_cost(self, current_cell, previous_cell) -> int:
        return 1

    @abstractmethod
    def __heuristic(self, current, target) -> int:
        return 0
