from unittest import TestCase

from ..src.TreeMapParser import TreeMapParser


class TestTreeMapParser(TestCase):
    def test_parse(self):
        lines = open('day8_treetop_tree_house/sample_input.txt', 'r').readlines()
        parser = TreeMapParser(lines)
        tree_map = parser.parse()
        self.assertListEqual([
            [3, 0, 3, 7, 3],
            [2, 5, 5, 1, 2],
            [6, 5, 3, 3, 2],
            [3, 3, 5, 4, 9],
            [3, 5, 3, 9, 0]],
            tree_map.map())
