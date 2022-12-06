from sys import stdin
from src.SupplyStacks import SupplyStacks9000, SupplyStacks9001


if __name__ == '__main__':
    supply_stacks_9000 = SupplyStacks9000()
    supply_stacks_9001 = SupplyStacks9001()
    loading_start_state = True
    for line in stdin:
        if loading_start_state:
            if line[1] == '1':
                # done with starting state load
                loading_start_state = False
            else:
                supply_stacks_9000.load_stack_level(line)
                supply_stacks_9001.load_stack_level(line)
        elif len(line.strip()) > 0:
            supply_stacks_9000.move_crates(line)
            supply_stacks_9001.move_crates(line)

    print(f'There are {supply_stacks_9000.stack_count()} supply stacks')
    print(f'The top crates using CrateMover 9000 are {supply_stacks_9000.top_crates()}')
    print(f'The top crates using CrateMover 9001 are {supply_stacks_9001.top_crates()}')
