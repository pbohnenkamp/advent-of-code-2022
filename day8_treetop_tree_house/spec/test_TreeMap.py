from unittest import TestCase

from ..src.TreeMap import TreeMap


class TestTreeMap(TestCase):
    def test_add_tree_row(self):
        my_tree_map = TreeMap()

        my_tree_map.add_tree_row([1, 2, 3, 4])
        self.assertListEqual([[1, 2, 3, 4]], my_tree_map.map())
        self.assertEqual(1, my_tree_map.tree_area_height())
        self.assertEqual(4, my_tree_map.tree_area_width())

        my_tree_map.add_tree_row([9, 8, 7, 6])
        self.assertListEqual([
            [1, 2, 3, 4],
            [9, 8, 7, 6]
        ], my_tree_map.map())
        self.assertEqual(2, my_tree_map.tree_area_height())
        self.assertEqual(4, my_tree_map.tree_area_width())

        with self.assertRaises(Exception):
            my_tree_map.add_tree_row([1, 2, 3])

    def test__is_tree_visible_from_north(self):
        my_tree_map = TreeMap()

        my_tree_map.add_tree_row([9, 0, 8, 2, 9, 9])
        my_tree_map.add_tree_row([9, 2, 6, 2, 9, 9])
        my_tree_map.add_tree_row([9, 4, 4, 3, 9, 9])
        my_tree_map.add_tree_row([9, 6, 2, 3, 9, 9])
        my_tree_map.add_tree_row([9, 9, 9, 9, 9, 9])

        self.assertListEqual([True, False, False, False],
                             [
                                 my_tree_map._is_tree_visible_from_north(1, 1),
                                 my_tree_map._is_tree_visible_from_north(1, 2),
                                 my_tree_map._is_tree_visible_from_north(1, 3),
                                 my_tree_map._is_tree_visible_from_north(1, 4),
                             ])
        self.assertListEqual([True, False, True, False],
                             [
                                 my_tree_map._is_tree_visible_from_north(2, 1),
                                 my_tree_map._is_tree_visible_from_north(2, 2),
                                 my_tree_map._is_tree_visible_from_north(2, 3),
                                 my_tree_map._is_tree_visible_from_north(2, 4),
                             ])
        self.assertListEqual([True, False, False, False],
                             [
                                 my_tree_map._is_tree_visible_from_north(3, 1),
                                 my_tree_map._is_tree_visible_from_north(3, 2),
                                 my_tree_map._is_tree_visible_from_north(3, 3),
                                 my_tree_map._is_tree_visible_from_north(3, 4),
                             ])

    def test__is_tree_visible_from_east(self):
        my_tree_map = TreeMap()

        my_tree_map.add_tree_row([9, 9, 9, 9, 9, 9])
        my_tree_map.add_tree_row([9, 4, 3, 2, 1, 0])
        my_tree_map.add_tree_row([9, 3, 2, 2, 1, 1])
        my_tree_map.add_tree_row([9, 9, 6, 0, 5, 0])
        my_tree_map.add_tree_row([9, 9, 9, 9, 9, 9])

        self.assertListEqual([True, True, True, True],
                             [
                                 my_tree_map._is_tree_visible_from_east(1, 1),
                                 my_tree_map._is_tree_visible_from_east(1, 2),
                                 my_tree_map._is_tree_visible_from_east(1, 3),
                                 my_tree_map._is_tree_visible_from_east(1, 4),
                             ])
        self.assertListEqual([True, False, True, False],
                             [
                                 my_tree_map._is_tree_visible_from_east(2, 1),
                                 my_tree_map._is_tree_visible_from_east(2, 2),
                                 my_tree_map._is_tree_visible_from_east(2, 3),
                                 my_tree_map._is_tree_visible_from_east(2, 4),
                             ])
        self.assertListEqual([True, True, False, True],
                             [
                                 my_tree_map._is_tree_visible_from_east(3, 1),
                                 my_tree_map._is_tree_visible_from_east(3, 2),
                                 my_tree_map._is_tree_visible_from_east(3, 3),
                                 my_tree_map._is_tree_visible_from_east(3, 4),
                             ])

    def test__is_tree_visible_from_south(self):
        my_tree_map = TreeMap()

        my_tree_map.add_tree_row([9, 9, 9, 9, 9, 9])
        my_tree_map.add_tree_row([9, 8, 2, 3, 9, 9])
        my_tree_map.add_tree_row([9, 6, 4, 3, 8, 9])
        my_tree_map.add_tree_row([9, 4, 6, 2, 8, 9])
        my_tree_map.add_tree_row([9, 2, 8, 2, 8, 9])

        self.assertListEqual([True, False, False, True],
                             [
                                 my_tree_map._is_tree_visible_from_south(1, 1),
                                 my_tree_map._is_tree_visible_from_south(1, 2),
                                 my_tree_map._is_tree_visible_from_south(1, 3),
                                 my_tree_map._is_tree_visible_from_south(1, 4),
                             ])
        self.assertListEqual([True, False, True, False],
                             [
                                 my_tree_map._is_tree_visible_from_south(2, 1),
                                 my_tree_map._is_tree_visible_from_south(2, 2),
                                 my_tree_map._is_tree_visible_from_south(2, 3),
                                 my_tree_map._is_tree_visible_from_south(2, 4),
                             ])
        self.assertListEqual([True, False, False, False],
                             [
                                 my_tree_map._is_tree_visible_from_south(3, 1),
                                 my_tree_map._is_tree_visible_from_south(3, 2),
                                 my_tree_map._is_tree_visible_from_south(3, 3),
                                 my_tree_map._is_tree_visible_from_south(3, 4),
                             ])

    def test__is_tree_visible_from_west(self):
        my_tree_map = TreeMap()

        my_tree_map.add_tree_row([9, 9, 9, 9, 9, 9])
        my_tree_map.add_tree_row([0, 2, 4, 6, 8, 9])
        my_tree_map.add_tree_row([8, 6, 4, 2, 0, 9])
        my_tree_map.add_tree_row([1, 1, 2, 2, 3, 9])
        my_tree_map.add_tree_row([9, 9, 9, 9, 9, 9])

        self.assertListEqual([True, True, True, True],
                             [
                                 my_tree_map._is_tree_visible_from_west(1, 1),
                                 my_tree_map._is_tree_visible_from_west(1, 2),
                                 my_tree_map._is_tree_visible_from_west(1, 3),
                                 my_tree_map._is_tree_visible_from_west(1, 4),
                             ])
        self.assertListEqual([False, False, False, False],
                             [
                                 my_tree_map._is_tree_visible_from_west(2, 1),
                                 my_tree_map._is_tree_visible_from_west(2, 2),
                                 my_tree_map._is_tree_visible_from_west(2, 3),
                                 my_tree_map._is_tree_visible_from_west(2, 4),
                             ])
        self.assertListEqual([False, True, False, True],
                             [
                                 my_tree_map._is_tree_visible_from_west(3, 1),
                                 my_tree_map._is_tree_visible_from_west(3, 2),
                                 my_tree_map._is_tree_visible_from_west(3, 3),
                                 my_tree_map._is_tree_visible_from_west(3, 4),
                             ])

    def test_count_visible_trees(self):
        my_tree_map = TreeMap()
        my_tree_map.add_tree_row([3, 0, 3, 7, 3])
        my_tree_map.add_tree_row([2, 5, 5, 1, 2])
        my_tree_map.add_tree_row([6, 5, 3, 3, 2])
        my_tree_map.add_tree_row([3, 3, 5, 4, 9])
        my_tree_map.add_tree_row([3, 5, 3, 9, 0])

        self.assertEqual(21, my_tree_map.count_visible_trees())

    def test_max_scenic_score(self):
        my_tree_map = TreeMap()
        my_tree_map.add_tree_row([3, 0, 3, 7, 3])
        my_tree_map.add_tree_row([2, 5, 5, 1, 2])
        my_tree_map.add_tree_row([6, 5, 3, 3, 2])
        my_tree_map.add_tree_row([3, 3, 5, 4, 9])
        my_tree_map.add_tree_row([3, 5, 3, 9, 0])

        self.assertEqual(8, my_tree_map.find_most_scenic_tree())
