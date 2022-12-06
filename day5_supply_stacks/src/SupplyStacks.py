from typing import List
from collections import deque


class SupplyStacks9000:
    def __init__(self) -> None:
        self._stack_list: List[SupplyStack] = []

    def load_stack_level(self, line: str):
        for i_stack_input in range(1, len(line), 4):
            crate_label = line[i_stack_input]
            stack_index = (i_stack_input // 4)
            self._push_crate_to_stack(stack_index, crate_label)

    def stack_count(self):
        return len(self._stack_list)

    def top_crates(self):
        return ''.join([stack.top_crate() for stack in self._stack_list])

    def move_crates(self, move_instruction: str):
        num_crates, from_stack, to_stack = self._parse_move_instruction(move_instruction)
        for i in range(num_crates):
            self._stack_list[to_stack].append(self._stack_list[from_stack].pop())

    def _push_crate_to_stack(self, stack_index: int, crate_label: str):
        if stack_index > len(self._stack_list) - 1:
            # need to add a new stack to stack list
            self._append_stack()
        if crate_label != ' ':
            self._stack_list[stack_index].push(crate_label)

    def _append_stack(self):
        self._stack_list.append(SupplyStack())

    @staticmethod
    def _parse_move_instruction(move_instruction):
        split_line = move_instruction.split()
        return int(split_line[1]), int(split_line[3]) - 1, int(split_line[5]) - 1

    def __getitem__(self, stack_index):
        return self._stack_list[stack_index]


class SupplyStack:
    def __init__(self) -> None:
        self._stack: deque[str] = deque()

    def crate_count(self):
        return len(self._stack)

    def push(self, crate_label):
        self._stack.appendleft(crate_label)

    def pop(self):
        return self._stack.pop()

    def append(self, crate_label):
        self._stack.append(crate_label)

    def __getitem__(self, crate_index):
        return self._stack[crate_index]

    def top_crate(self):
        return self._stack[-1]


class SupplyStacks9001(SupplyStacks9000):
    def move_crates(self, move_instruction: str):
        num_crates, from_stack, to_stack = self._parse_move_instruction(move_instruction)
        for crate in self._pick_up_crates(from_stack, num_crates):
            self._stack_list[to_stack].append(crate)

    def _pick_up_crates(self, stack_index, num_crates):
        crates = deque()
        for i in range(num_crates):
            crates.appendleft(self._stack_list[stack_index].pop())
        return list(crates)

