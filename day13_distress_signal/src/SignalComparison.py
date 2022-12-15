from collections import deque


class SignalComparison:
    def __init__(self, first_packet: str, second_packet: str) -> None:
        self.first_packet = first_packet
        self.second_packet = second_packet

    def are_packets_in_order(self):
        left = self._parse_packet_list(deque(self.first_packet))
        right = self._parse_packet_list(deque(self.second_packet))
        if self._lists_in_order(left, right) == -1:
            return False
        else:
            return True

    def _parse_packet_list(self, packet_deque: deque[str]):
        packet_list = []
        # remove the first bracket
        packet_deque.popleft()
        while not packet_deque[0] == ']':
            if packet_deque[0] == '[':
                packet_list.append(self._parse_packet_list(packet_deque))
            elif packet_deque[0].isdigit():
                digit_str = packet_deque.popleft()
                while packet_deque[0].isdigit():
                    digit_str += packet_deque.popleft()
                packet_list.append(int(digit_str))
            else:
                packet_deque.popleft()
        # remove the last bracket
        packet_deque.popleft()
        return packet_list

    def _lists_in_order(self, left, right):
        # 1 reps in order, 0 reps equal, -1 reps not equal
        are_in_order = 0  # assume equal to start
        for i, value in enumerate(left):
            if not len(right) > i:
                # right ran out before left, not in order
                are_in_order = -1
            elif isinstance(value, list):
                if isinstance(right[i], list):
                    are_in_order = self._lists_in_order(value, right[i])
                else:
                    are_in_order = self._lists_in_order(value, [right[i]])
            elif isinstance(right[i], list):
                are_in_order = self._lists_in_order([value], right[i])
            elif value < right[i]:
                are_in_order = 1
            elif value > right[i]:
                are_in_order = -1
            # analyze are_in_order, only continue if they are still equal
            if not are_in_order == 0:
                break
        # last rule, if left runs out before right and if they are still equal, they are in order
        if are_in_order == 0 and len(left) < len(right):
            are_in_order = 1
        return are_in_order
