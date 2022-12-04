from .RucksackItemType import RucksackItemType


class RucksackList:
    def __init__(self, rucksack_item_type_list) -> None:
        if len(rucksack_item_type_list) % 2 == 1:
            raise Exception('Rucksack item type lists must have an even number of items')

        self._compartment_1 = list(
            map(self._map_list_char_to_rucksack_item_type, rucksack_item_type_list[0:(len(rucksack_item_type_list) // 2)]))
        self._compartment_2 = list(
            map(self._map_list_char_to_rucksack_item_type, rucksack_item_type_list[(len(rucksack_item_type_list) // 2):]))

    def complete_type_set(self):
        return set(self.compartment_1_types_list() + self.compartment_2_types_list())

    def compartment_1_types_list(self):
        return self._compartment_1

    def compartment_2_types_list(self):
        return self._compartment_2

    def compartment_1_type_set(self):
        return set(self.compartment_1_types_list())

    def compartment_2_type_set(self):
        return set(self.compartment_2_types_list())

    def find_shared_types_between_compartments(self):
        return self.compartment_1_type_set().intersection(self.compartment_2_type_set())

    def _compartment_as_item_type_list(self, compartment):
        return ''.join(map(self._map_rucksack_item_type_to_list_char, compartment))

    @staticmethod
    def _map_list_char_to_rucksack_item_type(list_char):
        return RucksackItemType(list_char)

    @staticmethod
    def _map_rucksack_item_type_to_list_char(rucksack_item_type):
        return rucksack_item_type.type_symbol()
