from unittest import TestCase
from .RucksackItemType import RucksackItemType


class TestRucksackItemType(TestCase):
    def test_construction(self):
        with self.assertRaises(Exception):
            rucksack_item_type = RucksackItemType('1')
        with self.assertRaises(Exception):
            rucksack_item_type = RucksackItemType('aa')

    def test_type_symbol(self):
        rucksack_item_type = RucksackItemType('a')
        self.assertEqual('a', rucksack_item_type.type_symbol())

    def test_priority(self):
        self.assertEqual(1, RucksackItemType('a').priority())
        self.assertEqual(16, RucksackItemType('p').priority())
        self.assertEqual(26, RucksackItemType('z').priority())
        self.assertEqual(27, RucksackItemType('A').priority())
        self.assertEqual(42, RucksackItemType('P').priority())
        self.assertEqual(52, RucksackItemType('Z').priority())
