from collections import deque
from dataclasses import dataclass
from sys import maxsize
from typing import List, Iterable


@dataclass(unsafe_hash=True)
class Node:
    height: str
    x: int
    y: int


@dataclass
class VisitedNode(Node):
    counter: int

    def __init__(self, node: Node, counter) -> None:
        self.height = node.height
        self.x = node.x
        self.y = node.y
        self.counter = counter

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Node):
            return False

        return (self.x, self.y) == (o.x, o.y)


class Heightmap:
    _start: Node = None
    _end: Node = None

    def __init__(self) -> None:
        self._map: List[List[Node]] = []

    def add_row(self, nodes: List[Node]):
        if self._start is None or self._end is None:
            for node in nodes:
                if node.height == 'S':
                    self._start = node
                    node.height = 'a'
                elif node.height == 'E':
                    self._end = node
                    node.height = 'z'

        self._map.append(nodes)

    def get_start(self) -> Node:
        return self._start

    def get_end(self) -> Node:
        return self._end

    def get_map_height(self):
        return len(self._map)

    def get_map_width(self):
        return len(self._map[0]) if len(self._map) > 0 else 0

    def find_optimal_path(self, reverse_to_a: bool = False):
        start_node = self._start
        unvisited = set()
        unvisited.add(start_node)
        distances = dict()
        prev_nodes = dict()
        for y, line in enumerate(self._map):
            for x, vertices in enumerate(line):
                unvisited.add(self._map[y][x])
                distances[self._map[y][x]] = 0 if self._map[y][x].height == 'a' and reverse_to_a else maxsize
                prev_nodes[self._map[y][x]] = None
        distances[start_node] = 0

        while len(unvisited) > 0:
            current_node = None
            for node in unvisited:
                if current_node is None:
                    current_node = node
                elif distances[node] < distances[current_node]:
                    current_node = node
            unvisited.remove(current_node)

            adj_nodes = [adj_node for adj_node in self._get_adjacent_nodes(current_node) if
                         (self._reachable_from(adj_node, current_node))]
            for adj_node in adj_nodes:
                if adj_node in unvisited:
                    new_distance = distances[current_node] + 1
                    if new_distance < distances[adj_node]:
                        distances[adj_node] = new_distance
                        prev_nodes[adj_node] = current_node

        return self._compile_optimal_path(prev_nodes)

    def _compile_optimal_path(self, prev_nodes):
        path = deque()
        last_node = self._end
        while last_node is not None:
            path.appendleft(last_node)
            last_node = prev_nodes[last_node]

        return set(path)

    def _get_adjacent_nodes(self, current_node):
        nodes = []
        if current_node.x - 1 >= 0:
            nodes.append(self._map[current_node.y][current_node.x - 1])
        if current_node.y - 1 >= 0:
            nodes.append(self._map[current_node.y - 1][current_node.x])
        if current_node.x + 1 < self.get_map_width():
            nodes.append(self._map[current_node.y][current_node.x + 1])
        if current_node.y + 1 < self.get_map_height():
            nodes.append(self._map[current_node.y + 1][current_node.x])
        return nodes

    @staticmethod
    def _reachable_from(current_node, adj_node):
        if ord(current_node.height) - ord(adj_node.height) <= 1:
            return True
        else:
            return False


class HeightmapParser:
    def parse(self, lines: Iterable[str]) -> Heightmap:
        map = Heightmap()
        for y, line in enumerate(lines):
            row: List[Node] = []
            for x, char in enumerate(line.strip()):
                row.append(Node(char, x, y))
            map.add_row(row)

        return map
