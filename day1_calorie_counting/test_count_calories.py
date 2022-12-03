from unittest import TestCase
from .count_calories import CalorieCounter


class TestCalorieCounter(TestCase):
    def test_construction(self):
        calorie_counter = CalorieCounter()
        self.assertEqual(0, calorie_counter.total_calories)
        self.assertEqual(0, calorie_counter.current_elf_calories)
        self.assertEqual(0, calorie_counter.highest_elf_calories())
        self.assertEqual(0, calorie_counter.elf_count)

    def test_add_calories_to_current_elf(self):
        calorie_counter = CalorieCounter()
        calorie_counter.add_calories_to_current_elf(1)
        self.assertEqual(1, calorie_counter.current_elf_calories)
        self.assertEqual(0, calorie_counter.highest_elf_calories(),
                         'should not change highest count until current elf is wrapped up')
        self.assertEqual(0, calorie_counter.total_calories,
                         'should not change total calorie count until current elf is wrapped up')
        self.assertEqual(0, calorie_counter.elf_count, 'should not change elf count until current elf is wrapped up')
        self.assertEqual(0, len(calorie_counter._calorie_entries),
                         'should not add calorie entry until current elf is wrapped up')

        calorie_counter.add_calories_to_current_elf('100')
        self.assertEqual(101, calorie_counter.current_elf_calories)

    def test_wrap_up_current_elf(self):
        calorie_counter = CalorieCounter()
        calorie_counter.add_calories_to_current_elf(1)
        calorie_counter.wrap_up_current_elf()
        self.assertEqual(0, calorie_counter.current_elf_calories, 'should set to 0 for counting next elf')
        self.assertEqual(1, calorie_counter.highest_elf_calories(),
                         'should have stored the previous elf as the highest calorie count so far')
        self.assertEqual(1, calorie_counter.total_calories, 'should have updated total calorie count')
        self.assertEqual(1, calorie_counter.elf_count, 'should have updated the elf count')
        self.assertEqual(1, calorie_counter._calorie_entries[0], 'should have added the entry to _calorie_entries')

        calorie_counter.wrap_up_current_elf()
        # should be idempotent if called twice in a row
        self.assertEqual(0, calorie_counter.current_elf_calories, 'should be idempotent if called twice in a row')
        self.assertEqual(1, calorie_counter.highest_elf_calories(), 'should be idempotent if called twice in a row')
        self.assertEqual(1, calorie_counter.total_calories, 'should be idempotent if called twice in a row')
        self.assertEqual(1, calorie_counter.elf_count, 'should be idempotent if called twice in a row')
        self.assertEqual(1, len(calorie_counter._calorie_entries), 'should be idempotent if called twice in a row')

        calorie_counter.add_calories_to_current_elf(3)
        calorie_counter.wrap_up_current_elf()
        self.assertEqual(3, calorie_counter.highest_elf_calories(),
                         'should have stored the previous elf as the highest calorie count so far')
        self.assertEqual(4, calorie_counter.total_calories, 'should have updated total calorie count')
        self.assertEqual(2, calorie_counter.elf_count, 'should have updated the elf count')
        self.assertEqual(3, calorie_counter._calorie_entries[0],
                         'should have added the entry to _calorie_entries in descending order')
        self.assertEqual(1, calorie_counter._calorie_entries[1],
                         'should have added the entry to _calorie_entries in descending order')

        calorie_counter.add_calories_to_current_elf(1)
        calorie_counter.add_calories_to_current_elf(1)
        calorie_counter.wrap_up_current_elf()
        self.assertEqual(3, calorie_counter.highest_elf_calories(), 'should not have updated the highest calorie count')
        self.assertEqual(6, calorie_counter.total_calories, 'should have updated total calorie count')
        self.assertEqual(3, calorie_counter.elf_count, 'should have updated the elf count')
        self.assertEqual(3, calorie_counter._calorie_entries[0],
                         'should have added the entry to _calorie_entries in descending order')
        self.assertEqual(2, calorie_counter._calorie_entries[1],
                         'should have added the entry to _calorie_entries in descending order')
        self.assertEqual(1, calorie_counter._calorie_entries[2],
                         'should have added the entry to _calorie_entries in descending order')

    def test_top_three_elves_calories(self):
        calorie_counter = CalorieCounter()
        calorie_counter.add_calories_to_current_elf(1)
        calorie_counter.wrap_up_current_elf()
        self.assertEqual(1, calorie_counter.top_three_elves_calories())

        calorie_counter.add_calories_to_current_elf(10)
        calorie_counter.wrap_up_current_elf()
        self.assertEqual(11, calorie_counter.top_three_elves_calories())

        calorie_counter.add_calories_to_current_elf(7)
        calorie_counter.wrap_up_current_elf()
        self.assertEqual(18, calorie_counter.top_three_elves_calories())

        calorie_counter.add_calories_to_current_elf(3)
        calorie_counter.wrap_up_current_elf()
        self.assertEqual(20, calorie_counter.top_three_elves_calories())

