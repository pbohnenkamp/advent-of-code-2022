from collections import deque
from unittest import TestCase

from ..src.SignalComparison import SignalComparison


class TestSignalComparison(TestCase):
    def test__parse_packet_list(self):
        expected = [1, 1, 3, 1, 1]
        signal_compare = SignalComparison('', '')
        self.assertListEqual(expected, signal_compare._parse_packet_list(deque('[1,1,3,1,1]')))

        expected = [[1], [2, 3, 4]]
        self.assertListEqual(expected, signal_compare._parse_packet_list(deque('[[1],[2,3,4]]')))

        expected = [[8, 7, 6]]
        self.assertListEqual(expected, signal_compare._parse_packet_list(deque('[[8,7,6]]')))

        expected = [[[]]]
        self.assertListEqual(expected, signal_compare._parse_packet_list(deque('[[[]]]')))

        expected = [1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
        self.assertListEqual(expected, signal_compare._parse_packet_list(deque('[1,[2,[3,[4,[5,6,7]]]],8,9]')))

    def test_are_packets_in_order(self):
        signal_compare = SignalComparison('[1,1,3,1,1]', '[1,1,5,1,1]')
        self.assertTrue(signal_compare.are_packets_in_order())

        signal_compare = SignalComparison('[[1],[2,3,4]]', '[[1],4]')
        self.assertTrue(signal_compare.are_packets_in_order())

        signal_compare = SignalComparison('[9]', '[[8, 7, 6]]')
        self.assertFalse(signal_compare.are_packets_in_order())

        signal_compare = SignalComparison('[[4,4],4,4]', '[[4,4],4,4,4]')
        self.assertTrue(signal_compare.are_packets_in_order())

        signal_compare = SignalComparison('[7,7,7,7]', '[7,7,7]')
        self.assertFalse(signal_compare.are_packets_in_order())

        signal_compare = SignalComparison('[]', '[3]')
        self.assertTrue(signal_compare.are_packets_in_order())

        signal_compare = SignalComparison('[[[]]]', '[[]]')
        self.assertFalse(signal_compare.are_packets_in_order())

        signal_compare = SignalComparison('[1,[2,[3,[4,[5,6,7]]]],8,9]', '[1,[2,[3,[4,[5,6,0]]]],8,9]')
        self.assertFalse(signal_compare.are_packets_in_order())

        signal_compare = SignalComparison('[[],[[[10,4,7],[8,3],4,8]]]',
                                          '[[[[9,3,4],[]],3,[],0],[],[[[6],1,[8,8],[]],[2,4,7],1,3]]')
        self.assertTrue(signal_compare.are_packets_in_order())

        signal_compare = SignalComparison('[[[7,3,[]],0],[3,[2]]]',
                                          '[[[[10,1,7],[7]]],[[7,6,7]],[[3,[6,4],[9,9,5],[2,8,5,4]],10],[[[4,5,10,1,1],[4,10],[8,9],[6,8,1,6],9],[[8,9],4,[],1,1],[2,[6,0],10,[],8],2],[8,[[],2]]]')
        self.assertTrue(signal_compare.are_packets_in_order())
