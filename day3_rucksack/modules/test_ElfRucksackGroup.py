from unittest import TestCase
from .ElfRucksackGroup import ElfRucksackGroup
from .RucksackList import RucksackList
from .RucksackItemType import RucksackItemType


class TestElfRucksackGroup(TestCase):
    def test_elf_rucksack_group(self):
        rucksack_group = ElfRucksackGroup()
        rucksack_group.add_rucksack_to_group(RucksackList('vJrwpWtwJgWrhcsFMMfFFhFp'))
        rucksack_group.add_rucksack_to_group(RucksackList('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL'))
        rucksack_group.add_rucksack_to_group(RucksackList('PmmdzqPrVvPwwTWBwg'))

        self.assertEqual(3, len(rucksack_group))
        self.assertEqual(RucksackItemType('r'), rucksack_group.find_badge_item_type())

        with self.assertRaises(Exception):
            rucksack_group.add_rucksack_to_group(RucksackList('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn'))

        rucksack_group = ElfRucksackGroup()
        rucksack_group.add_rucksack_to_group(RucksackList('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn'))
        rucksack_group.add_rucksack_to_group(RucksackList('ttgJtRGJQctTZtZT'))

        self.assertEqual(2, len(rucksack_group))
        with self.assertRaises(Exception):
            self.assertEqual(RucksackItemType('Z'), rucksack_group.find_badge_item_type())

        rucksack_group.add_rucksack_to_group(RucksackList('CrZsJsPPZsGzwwsLwLmpwMDw'))
        self.assertEqual(RucksackItemType('Z'), rucksack_group.find_badge_item_type())
