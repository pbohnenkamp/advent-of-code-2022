from typing import List
from sys import stdin
from modules.RucksackList import RucksackList
from modules.ElfRucksackGroup import ElfRucksackGroup


class ElvesRucksackBadgePrioritizer:
    def __init__(self) -> None:
        self._rucksack_groups: List[ElfRucksackGroup] = []
        self._current_rucksack_group = ElfRucksackGroup()

    def add_rucksack(self, rucksack_item_list):
        self._current_rucksack_group.add_rucksack_to_group(RucksackList(rucksack_item_list))
        if len(self._current_rucksack_group) == 3:
            self._rucksack_groups.append(self._current_rucksack_group)
            self._current_rucksack_group = ElfRucksackGroup()

    def sum_badge_priorities(self):
        summed_priority = 0
        for rucksack_group in self._rucksack_groups:
            summed_priority += rucksack_group.find_badge_item_type().priority()
        return summed_priority


if __name__ == '__main__':
    prioritizer = ElvesRucksackBadgePrioritizer()
    for line in stdin:
        prioritizer.add_rucksack(line.strip())

    print(prioritizer.sum_badge_priorities())
