from sys import stdin

from src.MonkeyInputParser import MonkeyInputParser


def run_rounds(a_parser: MonkeyInputParser, num_rounds: int):
    a_parser.parse_input(lines.copy())

    part_two_modulo = 1
    for monkey in a_parser.monkeys:
        part_two_modulo *= monkey.get_test_divisor()

    print(f'Part two modulo {part_two_modulo}')
    for monkey in a_parser.monkeys:
        monkey.set_recipient(a_parser.monkeys[monkey.true_toss_index], True)
        monkey.set_recipient(a_parser.monkeys[monkey.false_toss_index], False)
        if not monkey.with_relief:
            monkey.set_worry_modulo(part_two_modulo)

    for toss_round in range(num_rounds):
        for monkey in a_parser.monkeys:
            monkey.take_turn()
        if (toss_round + 1) % 20 == 0:
            print(f'After {toss_round + 1} rounds:')
            for i, monkey in enumerate(a_parser.monkeys):
                print(f'Monkey {i} inspected items {a_parser.monkeys[i].item_inspection_count} times:')

    return sorted(a_parser.monkeys, key=lambda i_monkey: i_monkey.item_inspection_count)


if __name__ == '__main__':
    parser = MonkeyInputParser()
    lines = stdin.readlines()
    sorted_monkeys = run_rounds(parser, 20)

    print(
        f'The level of monkey business with relief is {sorted_monkeys[-1].item_inspection_count * sorted_monkeys[-2].item_inspection_count}')

    parser = MonkeyInputParser(False)
    sorted_monkeys = run_rounds(parser, 10000)

    print(
        f'The level of monkey business without relief is {sorted_monkeys[-1].item_inspection_count * sorted_monkeys[-2].item_inspection_count}')
