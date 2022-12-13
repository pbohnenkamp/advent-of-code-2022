from collections import deque
from math import floor
from typing import Callable, List, Union

from .Item import Item


class Monkey:
    def __init__(
            self,
            inspect_operation: Callable[[int], int],
            test_divisor: int,
            monkey_index: int,
            true_test_toss_index,
            false_test_toss_index,
            starting_items: List[Item] = None,
            with_relief: bool = True
    ) -> None:
        self._worry_modulo = None
        if starting_items is None:
            starting_items = []
        self._item_queue: deque[Item] = deque(starting_items)
        self._inspect_operation = inspect_operation
        self._test_divisor = test_divisor
        self._monkey_index = monkey_index
        self.item_inspection_count = 0
        self.true_toss_index = true_test_toss_index
        self.false_toss_index = false_test_toss_index
        self._true_toss_recipient: Union['Monkey', None] = None
        self._false_toss_recipient: Union['Monkey', None] = None
        self.with_relief = with_relief

    def set_recipient(self, monkey: 'Monkey', test_result: bool):
        if test_result:
            self._true_toss_recipient = monkey
        else:
            self._false_toss_recipient = monkey

    def set_worry_modulo(self, divisors_product):
        self._worry_modulo = divisors_product

    def take_turn(self):
        while self._item_queue:
            item = self._item_queue.popleft()
            self._inspect_item(item)
            self._toss_item(item)

    def _inspect_item(self, item):
        self.item_inspection_count += 1
        item.worry_level = self._inspect_operation(item.worry_level)

    def _toss_item(self, item):
        self._calculate_relief(item)
        if item.worry_level % self._test_divisor == 0:
            self._true_toss_recipient.catch_item(item)
        else:
            self._false_toss_recipient.catch_item(item)

    def _calculate_relief(self, item):
        if self.with_relief:
            item.worry_level = floor(item.worry_level / 3)
        else:
            # This is the magic for the second step. since all divisors are prime
            # we can reduce the worry by mod'ing it with the all the monkey's divisors
            # multiplied together
            item.worry_level = item.worry_level % self._worry_modulo

    def catch_item(self, item: Item):
        self._item_queue.append(item)

    def _string_mod_cheat(self, worry_level):
        # Initialize result
        res = 0

        # One by one process all digits
        # of 'worry_level'
        s_worry_level = str(worry_level)
        for i in range(0, len(s_worry_level)):
            res = (res * 10 + int(s_worry_level[i])) % self._test_divisor

        return res

    def get_test_divisor(self):
        return self._test_divisor
