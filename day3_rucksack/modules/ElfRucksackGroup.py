from typing import List
from .RucksackList import RucksackList


class ElfRucksackGroup:
    def __init__(self) -> None:
        self._rucksacks: List[RucksackList] = []

    def add_rucksack_to_group(self, rucksack_list: RucksackList):
        if len(self._rucksacks) == 3:
            raise Exception('An Elf Rucksack Group can contain at most three Rucksacks')
        self._rucksacks.append(rucksack_list)

    def find_badge_item_type(self):
        if not len(self._rucksacks) == 3:
            raise Exception('An Elf Rucksack Group must have three Rucksacks before a badge can be found')
        return list(self._rucksacks[0].complete_type_set().intersection(self._rucksacks[1].complete_type_set(),
                                                                        self._rucksacks[2].complete_type_set()))[0]

    def __len__(self):
        return len(self._rucksacks)
