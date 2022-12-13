from unittest import TestCase

from day11_monkey_in_middle.src.Item import Item
from day11_monkey_in_middle.src.Monkey import Monkey


class TestMonkey(TestCase):
    def test_take_turn(self):
        monkeys = [
            Monkey(lambda x: x * 19, 23, 0, 2, 3, [Item(79), Item(98)]),
            Monkey(lambda x: x + 6, 19, 1, 2, 0, [Item(54), Item(65), Item(75), Item(74)]),
            Monkey(lambda x: x * x, 13, 2, 1, 3, [Item(79), Item(60), Item(97)]),
            Monkey(lambda x: x + 3, 17, 3, 0, 1, [Item(74)])
        ]
        self.assertEqual(2, monkeys[0].true_toss_index)
        self.assertEqual(3, monkeys[0].false_toss_index)

        for monkey in monkeys:
            monkey.set_recipient(monkeys[monkey.true_toss_index], True)
            monkey.set_recipient(monkeys[monkey.false_toss_index], False)

        monkeys[0].take_turn()
        self.assertEqual(0, len(monkeys[0]._item_queue))
        self.assertEqual(500, monkeys[3]._item_queue[-2].worry_level)
        self.assertEqual(620, monkeys[3]._item_queue[-1].worry_level)
        self.assertEqual(2, monkeys[0].item_inspection_count)

        monkeys[1].take_turn()
        self.assertEqual(0, len(monkeys[1]._item_queue))
        self.assertEqual(20, monkeys[0]._item_queue[-4].worry_level)
        self.assertEqual(23, monkeys[0]._item_queue[-3].worry_level)
        self.assertEqual(27, monkeys[0]._item_queue[-2].worry_level)
        self.assertEqual(26, monkeys[0]._item_queue[-1].worry_level)
        self.assertEqual(4, monkeys[1].item_inspection_count)

        monkeys[2].take_turn()
        self.assertEqual(0, len(monkeys[2]._item_queue))
        self.assertEqual(2080, monkeys[1]._item_queue[-1].worry_level)
        self.assertEqual(1200, monkeys[3]._item_queue[-2].worry_level)
        self.assertEqual(3136, monkeys[3]._item_queue[-1].worry_level)
        self.assertEqual(3, monkeys[2].item_inspection_count)

        monkeys[3].take_turn()
        self.assertEqual(0, len(monkeys[3]._item_queue))
        self.assertEqual(25, monkeys[1]._item_queue[-5].worry_level)
        self.assertEqual(167, monkeys[1]._item_queue[-4].worry_level)
        self.assertEqual(207, monkeys[1]._item_queue[-3].worry_level)
        self.assertEqual(401, monkeys[1]._item_queue[-2].worry_level)
        self.assertEqual(1046, monkeys[1]._item_queue[-1].worry_level)
        self.assertEqual(5, monkeys[3].item_inspection_count)

        for toss_round in range(19):
            for monkey in monkeys:
                monkey.take_turn()

        self.assertEqual(101, monkeys[0].item_inspection_count)
        self.assertEqual(95, monkeys[1].item_inspection_count)
        self.assertEqual(7, monkeys[2].item_inspection_count)
        self.assertEqual(105, monkeys[3].item_inspection_count)

    def test_take_turn_second_worry_strategy(self):
        monkeys = [
            Monkey(lambda x: x * 19, 23, 0, 2, 3, [Item(79), Item(98)], False),
            Monkey(lambda x: x + 6, 19, 1, 2, 0, [Item(54), Item(65), Item(75), Item(74)], False),
            Monkey(lambda x: x * x, 13, 2, 1, 3, [Item(79), Item(60), Item(97)], False),
            Monkey(lambda x: x + 3, 17, 3, 0, 1, [Item(74)], False)
        ]
        self.assertEqual(2, monkeys[0].true_toss_index)
        self.assertEqual(3, monkeys[0].false_toss_index)

        for monkey in monkeys:
            monkey.set_recipient(monkeys[monkey.true_toss_index], True)
            monkey.set_recipient(monkeys[monkey.false_toss_index], False)
            monkey.set_worry_modulo(23 * 19 * 13 * 17)

        monkeys[0].take_turn()
        self.assertEqual(0, len(monkeys[0]._item_queue))
        self.assertEqual(1501, monkeys[3]._item_queue[-2].worry_level)
        self.assertEqual(1862, monkeys[3]._item_queue[-1].worry_level)
        self.assertEqual(2, monkeys[0].item_inspection_count)
        monkeys[1].take_turn()
        monkeys[2].take_turn()
        monkeys[3].take_turn()

        for toss_round in range(19):
            for monkey in monkeys:
                monkey.take_turn()

        self.assertEqual(99, monkeys[0].item_inspection_count)
        self.assertEqual(97, monkeys[1].item_inspection_count)
        self.assertEqual(8, monkeys[2].item_inspection_count)
        self.assertEqual(103, monkeys[3].item_inspection_count)
