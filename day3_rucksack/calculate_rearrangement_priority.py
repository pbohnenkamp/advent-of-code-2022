from sys import stdin
from modules.RucksackList import RucksackList


class ElvesRucksackErrorsPrioritizer:
    def __init__(self) -> None:
        self._rucksacks = []

    def add_rucksack(self, rucksack_item_list):
        self._rucksacks.append(RucksackList(rucksack_item_list))

    def sum_error_priorities(self):
        summed_priority = 0
        for rucksack in self._rucksacks:
            for error_type in rucksack.find_shared_types_between_compartments():
                summed_priority += error_type.priority()
        return summed_priority


if __name__ == '__main__':
    prioritizer = ElvesRucksackErrorsPrioritizer()
    for line in stdin:
        prioritizer.add_rucksack(line.strip())

    print(prioritizer.sum_error_priorities())
