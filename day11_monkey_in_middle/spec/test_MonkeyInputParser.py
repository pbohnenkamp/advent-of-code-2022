from unittest import TestCase

from day11_monkey_in_middle.src.MonkeyInputParser import MonkeyInputParser


class TestMonkeyInputParser(TestCase):
    def test_parse_input(self):
        fo = open('../sample_input.txt', 'r')
        lines = fo.readlines()
        parser = MonkeyInputParser()
        parser.parse_input(lines)
        fo.close()

        for monkey in parser.monkeys:
            monkey.set_recipient(parser.monkeys[monkey.true_toss_index], True)
            monkey.set_recipient(parser.monkeys[monkey.false_toss_index], False)

        for toss_round in range(20):
            for monkey in parser.monkeys:
                monkey.take_turn()

        self.assertEqual(101, parser.monkeys[0].item_inspection_count)
        self.assertEqual(95, parser.monkeys[1].item_inspection_count)
        self.assertEqual(7, parser.monkeys[2].item_inspection_count)
        self.assertEqual(105, parser.monkeys[3].item_inspection_count)
