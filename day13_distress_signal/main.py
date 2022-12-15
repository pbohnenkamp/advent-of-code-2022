import functools
from collections import deque
from sys import stdin

from src.SignalComparison import SignalComparison

if __name__ == '__main__':
    lines = stdin.readlines()
    deque_lines = deque(lines)
    pair_index = 1
    sum_ordered_packets = 0
    all_packets = []
    while len(deque_lines) > 0:
        if deque_lines[0].strip() == '':
            deque_lines.popleft()
        pair = [deque_lines.popleft().strip(), deque_lines.popleft().strip()]
        if SignalComparison(pair[0], pair[1]).are_packets_in_order():
            sum_ordered_packets += pair_index
        all_packets += [pair[0], pair[1]]
        pair_index += 1

    print(f'The sum of the in order packet indexes is {sum_ordered_packets}')

    # part 2
    all_packets += ['[[2]]', '[[6]]']

    all_packets.sort(key=functools.cmp_to_key(lambda a, b: - 1 if SignalComparison(a, b).are_packets_in_order() else 1))

    decoder = 1
    for i, packet in enumerate(all_packets):
        if packet == '[[2]]':
            decoder *= i + 1
        if packet == '[[6]]':
            decoder *= i + 1
            break

    print(f'The decoder key is {decoder}')
