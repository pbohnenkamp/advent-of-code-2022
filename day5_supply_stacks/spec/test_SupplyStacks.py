from unittest import TestCase
import os
from ..src.SupplyStacks import SupplyStacks9000, SupplyStacks9001


class TestSupplyStacks(TestCase):
    def test_simple_load_stack_levels(self):
        supply_stacks = SupplyStacks9000()

        # load an initial single stack
        supply_stacks.load_stack_level('[A]')

        self.assertEqual(1, supply_stacks.stack_count())
        self.assertEqual(1, supply_stacks[0].crate_count())
        self.assertEqual('A', supply_stacks[0][0])
        self.assertEqual('A', supply_stacks[0].top_crate())
        self.assertEqual('A', supply_stacks.top_crates())

        # add a crate to it
        supply_stacks.load_stack_level('[B]')
        self.assertEqual(1, supply_stacks.stack_count())
        self.assertEqual(2, supply_stacks[0].crate_count())
        self.assertEqual('B', supply_stacks[0][0])
        self.assertEqual('A', supply_stacks[0][1])
        self.assertEqual('A', supply_stacks[0].top_crate())
        self.assertEqual('A', supply_stacks.top_crates())

        # pop off a crate
        self.assertEqual('A', supply_stacks[0].pop())
        self.assertEqual(1, supply_stacks[0].crate_count())

    # add another two stacks
        supply_stacks.load_stack_level('    [M] [X]')
        self.assertEqual(3, supply_stacks.stack_count())
        self.assertEqual(1, supply_stacks[0].crate_count())
        self.assertEqual('M', supply_stacks[1].top_crate())
        self.assertEqual(1, supply_stacks[1].crate_count())
        self.assertEqual('X', supply_stacks[2].top_crate())
        self.assertEqual(1, supply_stacks[2].crate_count())
        self.assertEqual('BMX', supply_stacks.top_crates())

    def test_parse_instruction(self):
        supply_stacks = SupplyStacks9000()

        self.assertTupleEqual((1, 1, 0), supply_stacks._parse_move_instruction('move 1 from 2 to 1'))

    def test_sample_9000(self):
        supply_stacks = SupplyStacks9000()
        file1 = open('day5_supply_stacks/sample_input.txt', 'r')
        Lines = file1.readlines()
        loading_start_state = True
        for line in Lines:
            if loading_start_state:
                if line[1] == '1':
                    # done with starting state load
                    loading_start_state = False
                else:
                    supply_stacks.load_stack_level(line)
            elif len(line.strip()) > 0:
                supply_stacks.move_crates(line)

        self.assertEqual(3, supply_stacks.stack_count())
        self.assertEqual('CMZ', supply_stacks.top_crates())

    def test_sample_9001(self):
        supply_stacks = SupplyStacks9001()
        file1 = open('day5_supply_stacks/sample_input.txt', 'r')
        Lines = file1.readlines()
        loading_start_state = True
        for line in Lines:
            if loading_start_state:
                if line[1] == '1':
                    # done with starting state load
                    loading_start_state = False
                else:
                    supply_stacks.load_stack_level(line)
            elif len(line.strip()) > 0:
                supply_stacks.move_crates(line)

        self.assertEqual(3, supply_stacks.stack_count())
        self.assertEqual('MCD', supply_stacks.top_crates())

