from typing import Any

from utils.data_structures.tags import Tags


class Node(Tags):
    def __init__(self, value: Any):
        super().__init__()
        self.__incoming_nodes = []
        self.__outgoing_nodes = []
        self.__incoming_edges = []
        self.__outgoing_edges = []
        self.update_tag({"value": value})

    def __repr__(self) -> str:
        return str(self.get("value")) if self.get("value") is not None else " "

    def add_connection(self, other, edge, is_source: bool):
        """
        Add a connection form the current Node to another Node (could be self)

        :param other: The other Node
        :param edge: The Edge connecting the Nodes
        :param is_source: True if the current Node is the source of the Edge, False if it is the target of the edge
        """
        if is_source:
            self.__outgoing_nodes.append(other)
            self.__outgoing_edges.append(edge)
        else:
            self.__incoming_nodes.append(other)
            self.__incoming_edges.append(edge)

    def is_connected(self, other) -> bool:
        """
        Check if a node is connected to this Node

        :param other: A Node to check if it is connected to this Node
        :return: Boolean True if the given Node is connected to this Node
        """
        return other in self.__outgoing_nodes or other in self.__incoming_nodes

    @property
    def indegree(self) -> int:
        """
        Gives the indegree (number of incoming edges) of the current Node
        """
        return len(self.__incoming_nodes)

    @property
    def outdegree(self) -> int:
        """
        Gives the outdegree (number of outgoing edges) of the current Node
        """
        return len(self.__outgoing_nodes)

    @property
    def outgoing_nodes(self) -> list:
        """
        Get a list of all outgoing Nodes

        :return: A list of all Nodes that are directly reachable from this Node
        """
        return self.__outgoing_nodes

    @property
    def incomming_nodes(self) -> list:
        """
        Get a list of all incomming Nodes

        :return: A list of all Nodes that can directly reach this Node
        """
        return self.__incoming_nodes

    @property
    def outgoing_connections(self) -> list:
        """
        Get a list of all outgoing connections

        :return: A list of all connected Nodes and the Edges connecting them in format [(n1, e1), (n2, e2), ...]
        """
        return [(node, edge) for node, edge in zip(self.__outgoing_nodes, self.__outgoing_edges)]

    @property
    def incomming_connections(self) -> list:
        """
        Get a list of all incomming connections

        :return: A list of all connected Nodes and the Edges connecting them in format [(n1, e1), (n2, e2), ...]
        """
        return [(node, edge) for node, edge in zip(self.__incoming_nodes, self.__incoming_edges)]

    @property
    def all_connections(self) -> list:
        """
        Get a list of all outgoing connections

        :return: A list of all connected Nodes and the Edges connecting them in format [(n1, e1), (n2, e2), ...]
        """
        all_connections = self.incomming_connections
        all_connections.extend(self.outgoing_connections)
        return all_connections


class Edge(Tags):
    def __init__(self, source: Node, target: Node, bidirectional: bool):
        super().__init__()
        self.source = source
        self.target = target
        # Default tag
        self.update_tag({"directed": bidirectional})

    def __repr__(self) -> str:
        return f"<'{self.source}'to'{self.target}'>"


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def find_node(self, tags: dict) -> Node | None:
        """
        Searches for a node with corresponding key-value tags

        :param tags: The given search criteria
        :return: Node that corresponds to all given tags, or None if no such Node can be found
        """
        for node in self.nodes:
            if all(node.get(key) == value for key, value in tags.items()):
                return node
        return None

    def add_connection(self, source: Node, target: Node, bidirectional: bool = False, tags: dict = None) -> None:
        """
        Add a connection to the graph between two Nodes

        :param source: The start Node of the new connection
        :param target: The end Node of the new connection
        :param bidirectional: directed edge?
        :param tags: optional tags for the edge
        """
        new_edge = Edge(source, target, bidirectional)
        new_edge.update_tag(tags)
        source.add_connection(target, new_edge, True)
        target.add_connection(source, new_edge, False)
        if bidirectional:
            source.add_connection(target, new_edge, False)
            target.add_connection(source, new_edge, True)
        self.edges.append(new_edge)

    def dijkstra(self, source: Node, target: Node) -> int:
        """
        Find the shortest path from the source to the target.
        Edges must have a non-negative 'value'

        :param source: Starting node
        :param target: Ending node
        :return: The shortest path from start to end
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"Graph(nodes({len(self.nodes)})={self.nodes}; edges({len(self.edges)})={self.edges})"


def build_graph(data: list, bidirectional: bool = False) -> Graph:
    """
    Example function on how to contruct a graph using data

    :param data: A list of connections
    where the first index represents the source Node and the last index represents the target Node
    :param bidirectional: True if the given connections are bidirectional
    :return: A graph constructed from the connections in the given list
    """
    graph = Graph()
    for line in data:
        s = graph.find_node({"value": line[0]})
        if s is None:
            s = Node(line[0])
            graph.nodes.append(s)
        e = graph.find_node({"value": line[-1]})
        if e is None:
            e = Node(line[-1])
            graph.nodes.append(e)
        graph.add_connection(source=s, target=e, bidirectional=bidirectional)
    return graph


if __name__ == "__main__":
    # Example data; Assume graph is build from the edges
    d = [
        "A -> B",
        "B -> C",
        "B -> D",
        "C -> D"
    ]
    g = build_graph(d)
    print(g)
    print(f"B is connected to: {g.find_node({'value': 'B'}).outgoing_nodes}")
