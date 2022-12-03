from sys import stdin
from collections import deque


class CalorieCounter:
    def __init__(self) -> None:
        self.elf_count = 0
        self._calorie_entries = deque()
        self.current_elf_calories = 0
        self.total_calories = 0

    def add_calories_to_current_elf(self, calories):
        self.current_elf_calories += int(calories)

    def wrap_up_current_elf(self):
        # check prevents two blank lines from counting a nonexistent elf
        if self.current_elf_calories > 0:
            self._add_elfs_total_calorie_count(self.current_elf_calories)
            self.elf_count += 1
            self.total_calories += self.current_elf_calories
            print(f'Elf {self.elf_count} was carrying {self.current_elf_calories}. The highest count so far is {self.highest_elf_calories()}')
            self.current_elf_calories = 0

    def highest_elf_calories(self):
        return self._calorie_entries[0] if self.elf_count > 0 else 0

    def top_three_elves_calories(self):
        count = 0
        for i in range(min(len(self._calorie_entries), 3)):
            count += self._calorie_entries[i]
        return count

    def _add_elfs_total_calorie_count(self, elfs_total_calories):
        for i in range(self.elf_count):
            if self._calorie_entries[i] < elfs_total_calories:
                self._calorie_entries.insert(i, elfs_total_calories)
                return  # added, break out of method
        # case where this entry is the lowest yet
        self._calorie_entries.append(elfs_total_calories)


def is_calorie_record(line):
    return len(line.strip()) > 0


def count_calories():
    calorie_counter = CalorieCounter()

    for line in stdin:
        if is_calorie_record(line):
            calorie_counter.add_calories_to_current_elf(line)
        else:
            calorie_counter.wrap_up_current_elf()

    calorie_counter.wrap_up_current_elf()

    print(f'The calorie total of the elf carrying the most calories is {calorie_counter.highest_elf_calories()}.')
    print(f'The calorie total of the top three elves is {calorie_counter.top_three_elves_calories()}.')
    print(f'There were {calorie_counter.elf_count} elves carrying a total of {calorie_counter.total_calories}.')


if __name__ == '__main__':
    count_calories()
