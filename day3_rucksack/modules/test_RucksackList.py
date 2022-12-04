from unittest import TestCase
from .RucksackList import RucksackList
from .RucksackItemType import RucksackItemType


class TestRucksackList(TestCase):
    def test_rucksack_list(self):
        input_1 = 'vJrwpWtwJgWr'
        input_1_type_set = set()
        input_1_type_list = []
        for type_char in input_1:
            item_type = RucksackItemType(type_char)
            input_1_type_set.add(item_type)
            input_1_type_list.append(item_type)

        input_2 = 'hcsFMMfFFhFp'
        input_2_type_set = set()
        input_2_type_list = []
        for type_char in input_2:
            item_type = RucksackItemType(type_char)
            input_2_type_set.add(item_type)
            input_2_type_list.append(item_type)

        all_types_set = set()
        for type_char in input_1 + input_2:
            all_types_set.add(RucksackItemType(type_char))

        rucksack_list = RucksackList(input_1 + input_2)
        self.assertListEqual(input_1_type_list, rucksack_list.compartment_1_types_list())
        self.assertSetEqual(input_1_type_set, rucksack_list.compartment_1_type_set())
        self.assertListEqual(input_2_type_list, rucksack_list.compartment_2_types_list())
        self.assertSetEqual(input_2_type_set, rucksack_list.compartment_2_type_set())
        self.assertSetEqual({RucksackItemType('p')}, rucksack_list.find_shared_types_between_compartments())
        self.assertSetEqual(all_types_set, rucksack_list.complete_type_set())

        with self.assertRaises(Exception):
            RucksackList('vJr')
