from utils.decorators import timer, debug
from utils.task import Task
from utils.data_structures.graph import Graph, build_graph


class Task11(Task):
    # Task constants
    YEAR = 2025
    TASK_NUM = 11

    def preprocess(self, data: list) -> Graph:
        connections = []
        for device in data:
            source = device[0][:-1]
            for target in device[1:]:
                connections.append((source, target))
        graph = build_graph(connections, bidirectional=False)
        return graph

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: Graph) -> int:
        start = data.find_node({"value": "you" if not self.IS_TEST else "svr"})
        return self.num_paths(start, data.find_node({"value": "out"}))

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: Graph) -> int:
        start = data.find_node({"value": "svr"})
        fft = data.find_node({"value": "fft"})
        dac = data.find_node({"value": "dac"})
        target = data.find_node({"value": "out"})
        paths_from_start_to_fft = self.num_paths(start, fft)
        for node in data.nodes:
            node.update_tag({"count": 0})
        paths_from_fft_dac = self.num_paths(fft, dac)
        for node in data.nodes:
            node.update_tag({"count": 0})
        paths_from_dac_to_out = self.num_paths(dac, target)
        for node in data.nodes:
            node.update_tag({"count": 0})
        return paths_from_start_to_fft * paths_from_fft_dac * paths_from_dac_to_out

    def num_paths(self, source, target) -> int:
        """
        Determine the number of possible (unique) paths from source to target.
        Cannot have loops

        :param source: The starting node of the path
        :param target: The ending node of the path
        :return: Number of possible paths from source to target
        """
        start = source
        start.update_tag({"count": 1})
        todo = [start]
        # Keep track of which node still be to be processed to maintain the correct operating order
        to_go = self.get_to_go(source, target)
        # Regular pathfinding algorithm
        while len(todo) > 0:
            node = todo.pop(0)
            if node == target:
                continue
            to_go.remove(node)
            count = node.get("count")
            for neighbor in node.outgoing_nodes:
                previous_count = neighbor.get("count")
                neighbor.update_tag({"count": count if previous_count is None else previous_count + count})
                # Check if any other nodes need to be processed before this neighbor can be processed
                if any([before in to_go for before in neighbor.incomming_nodes]):
                    continue
                else:
                    todo.append(neighbor)
        return target.get("count")

    @staticmethod
    def get_to_go(source, target) -> set:
        """
        Find all nodes that will be visited when searching a path from source to target

        :param source:
        :param target:
        :return:
        """
        start = source
        start.update_tag({"count": 1})
        todo = [start]
        seen = set()
        while len(todo) > 0:
            node = todo.pop(0)
            seen.add(node)
            if node == target:
                continue
            for neighbor in node.outgoing_nodes:
                if neighbor not in seen and neighbor not in todo:
                    todo.append(neighbor)
        return seen


if __name__ == "__main__":
    # Load task
    t = Task11()

    # Run task
    t.run_all()
