from typing import Iterable

from .TreeMap import TreeMap


class TreeMapParser:
    def __init__(self, map_lines: Iterable[str]) -> None:
        self._map_lines = map_lines
        self._tree_map = TreeMap()

    def parse(self):
        for trimmed_map_line in [map_line.strip() for map_line in self._map_lines]:
            self._tree_map.add_tree_row([int(height) for height in trimmed_map_line])

        return self._tree_map
