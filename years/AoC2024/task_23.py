from utils.decorators import timer, debug
from utils.task import Task


class Task23(Task):
    # Task constants
    YEAR = 2024
    TASK_NUM = 23

    def preprocess(self, data: list) -> list:
        ts = []
        connections = []
        for line in data:
            comp1, comp2 = line.split('-')
            connections.append((comp1, comp2))
            if comp1[0] == "t" and comp1 not in ts:
                ts.append(comp1)
            if comp2[0] == "t" and comp2 not in ts:
                ts.append(comp2)
        return [connections, ts]

    @debug
    @timer(YEAR, TASK_NUM)
    def part_1(self, data: list) -> int:
        sets = set()
        for t_comp in data[1]:
            current_connections = []
            for connection in data[0]:
                connected = connection[0] if connection[1] == t_comp else connection[1]
                if t_comp in connection:
                    for possible_3rd in current_connections:
                        if (connected, possible_3rd) in data[0] or (possible_3rd, connected) in data[0]:
                            sets.add(tuple(sorted((t_comp, connected, possible_3rd))))
                    current_connections.append(connected)
        return len(sets)

    @debug
    @timer(YEAR, TASK_NUM)
    def part_2(self, data: list) -> str:
        if len(data[0]) > 50:
            connections = data[0]
            comps = self.get_computers(connections)
            for comp in comps:
                neighbors = self.node_neighbors(connections, comp)
                for neighbor in neighbors:
                    clique = neighbors.copy()
                    clique.remove(neighbor)
                    clique.append(comp)
                    if len(clique) == 13 and self.is_clique(connections, clique):
                        return ",".join(sorted(clique))
        else:
            connections = data[0]
            comps = self.get_computers(connections)
            cliques = self.find_max_cliques(connections, comps)[0]
            return ",".join(sorted(cliques))

    @staticmethod
    def node_neighbors(connections: list, node: str):
        neighbors = []
        for connect in connections:
            if connect[0] == node:
                neighbors.append(connect[1])
            if connect[1] == node:
                neighbors.append(connect[0])
        return neighbors

    def find_max_cliques(self, connections: list, nodes: list) -> list:
        possible_cliques = [[node] for node in nodes.copy()]
        i = 0
        while len(possible_cliques) > 0:
            new_possible_cliques = []
            for clique in possible_cliques:
                for node in nodes:
                    if node <= clique[-1]:
                        continue
                    try_clique = clique.copy()
                    try_clique.append(node)
                    if self.is_clique(connections, try_clique):
                        new_possible_cliques.append(try_clique)
            if len(new_possible_cliques) == 0:
                return possible_cliques
            i += 1
            possible_cliques = new_possible_cliques

    @staticmethod
    def is_clique(connections: list, computers: list) -> bool:
        for comp in computers:
            for other_comp in computers:
                if comp != other_comp and not ((comp, other_comp) in connections or (other_comp, comp) in connections):
                    return False
        return True

    @staticmethod
    def get_computers(connections: list) -> list:
        computers = []
        for connection in connections:
            if connection[0] not in computers:
                computers.append(connection[0])
            if connection[1] not in computers:
                computers.append(connection[1])
        return computers


if __name__ == "__main__":
    # Load task
    t = Task23()

    # Run task
    t.run_all()
