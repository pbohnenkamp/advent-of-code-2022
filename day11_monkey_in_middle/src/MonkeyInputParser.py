from collections import deque
from typing import Iterable

from .Item import Item
from .Monkey import Monkey


class MonkeyInputParser:
    def __init__(self, with_relief: bool = True) -> None:
        self.monkeys = []
        self._with_relief = with_relief

    def parse_input(self, lines: Iterable[str]):
        d_lines = deque(lines)
        monkey_count = 0
        while d_lines:
            line = d_lines.popleft()
            if line.startswith('Monkey'):
                self._add_monkey(d_lines, monkey_count)
                monkey_count += 1

    def _add_monkey(self, d_lines, monkey_count):
        starting_items = self._parse_starting_items(d_lines.popleft())
        operation = self._parse_operation(d_lines.popleft())
        test_divisor = self._parse_test_divisor(d_lines.popleft())
        true_monkey = self._parse_throw_to(d_lines.popleft())
        false_monkey = self._parse_throw_to(d_lines.popleft())
        self.monkeys.append(
            Monkey(operation, test_divisor, monkey_count, true_monkey, false_monkey, starting_items, self._with_relief))

    @staticmethod
    def _parse_starting_items(line):
        items_strs = line.strip()[len('Starting items: '):].split(', ')
        return [Item(int(i)) for i in items_strs]

    @staticmethod
    def _parse_operation(line):
        op = line.strip()[len('Operation: new = '):]
        d = {}
        exec("def f(old): return " + op, d)
        return d['f']

    @staticmethod
    def _parse_test_divisor(line):
        return int(line.strip()[len('Test: divisible by '):])

    @staticmethod
    def _parse_throw_to(line):
        return int(line.strip().split(' ')[-1])
