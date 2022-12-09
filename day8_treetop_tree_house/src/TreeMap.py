import copy
from math import prod
from typing import List


class TreeMap:

    def __init__(self) -> None:
        self._map: List[List: int] = []
        self._tree_area_width = 0

    def tree_area_height(self):
        return len(self._map)

    def tree_area_width(self):
        return self._tree_area_width

    def add_tree_row(self, map_row: List[int]):
        if self._tree_area_width == 0:
            self._tree_area_width = len(map_row)
        elif self._tree_area_width != len(map_row):
            raise Exception('All the rows of a TreeMap must have the same width (number of columns)')

        self._map.append(map_row)

    def map(self):
        return copy.deepcopy(self._map)

    def count_visible_trees(self):
        running_count = self._count_all_edge_trees()
        for i in range(1, self.tree_area_height() - 1):
            for j in range(1, self.tree_area_width() - 1):
                if self._is_tree_visible(i, j):
                    running_count += 1

        return running_count

    def find_most_scenic_tree(self):
        max_scenic_tree_score = 1
        for i in range(1, self.tree_area_height() - 1):
            for j in range(1, self.tree_area_width() - 1):
                scenic_tree_score = prod([
                    self._trees_visible_to_north(i, j),
                    self._trees_visible_to_east(i, j),
                    self._trees_visible_to_south(i, j),
                    self._trees_visible_to_west(i, j)
                ])
                if scenic_tree_score > max_scenic_tree_score:
                    max_scenic_tree_score = scenic_tree_score
        return max_scenic_tree_score

    def _count_all_edge_trees(self):
        return self.tree_area_width() * 2 + (self.tree_area_height() - 2) * 2

    def _is_tree_visible(self, i, j):
        return any([
            self._is_tree_visible_from_north(i, j),
            self._is_tree_visible_from_east(i, j),
            self._is_tree_visible_from_south(i, j),
            self._is_tree_visible_from_west(i, j)
        ])

    def _is_tree_visible_from_north(self, i, j):
        tree_height = self._map[i][j]
        tree_heights_to_north = self._tree_heights_to_north(i, j)
        return max(tree_heights_to_north) < tree_height

    def _tree_heights_to_north(self, i, j):
        return [self._map[n][j] for n in range(i - 1, -1, -1)]

    def _is_tree_visible_from_east(self, i, j):
        tree_height = self._map[i][j]
        tree_heights_to_east = self._tree_heights_to_east(i, j)
        return max(tree_heights_to_east) < tree_height

    def _tree_heights_to_east(self, i, j):
        return [self._map[i][n] for n in range(j + 1, self.tree_area_width())]

    def _is_tree_visible_from_south(self, i, j):
        tree_height = self._map[i][j]
        tree_heights_to_south = self._tree_heights_to_south(i, j)
        return max(tree_heights_to_south) < tree_height

    def _tree_heights_to_south(self, i, j):
        return [self._map[n][j] for n in range(i + 1, self.tree_area_height())]

    def _is_tree_visible_from_west(self, i, j):
        tree_height = self._map[i][j]
        tree_heights_to_west = self._tree_heights_to_west(i, j)
        return max(tree_heights_to_west) < tree_height

    def _tree_heights_to_west(self, i, j):
        return [self._map[i][n] for n in range(j - 1, -1, -1)]

    def _trees_visible_to_north(self, i, j):
        tree_height = self._map[i][j]
        tree_heights_to_north = self._tree_heights_to_north(i, j)
        return self._count_visible_trees(tree_height, tree_heights_to_north)

    def _trees_visible_to_east(self, i, j):
        tree_height = self._map[i][j]
        tree_heights_to_east = self._tree_heights_to_east(i, j)
        return self._count_visible_trees(tree_height, tree_heights_to_east)

    def _trees_visible_to_south(self, i, j):
        tree_height = self._map[i][j]
        tree_heights_to_south = self._tree_heights_to_south(i, j)
        return self._count_visible_trees(tree_height, tree_heights_to_south)

    def _trees_visible_to_west(self, i, j):
        tree_height = self._map[i][j]
        tree_heights_to_west = self._tree_heights_to_west(i, j)
        return self._count_visible_trees(tree_height, tree_heights_to_west)

    @staticmethod
    def _count_visible_trees(tree_height, tree_heights_in_direction):
        visible_count = 0
        for other_tree_height in tree_heights_in_direction:
            if other_tree_height >= tree_height:
                visible_count += 1
                break
            else:
                visible_count += 1
        return visible_count
