from unittest import TestCase
from ..src.TuningBufferReader import TuningBufferReader, TuningBufferReaderNoStartPacketError


class TestTuningBufferReader(TestCase):
    def test_find_start_of_packet_marker_happy_path(self):
        tbr = TuningBufferReader('abcd')
        self.assertEqual(4, tbr.find_start_of_packet_marker())

    def test_find_start_of_packet_marker_repeats(self):
        tbr = TuningBufferReader('mmmmbbbccdef')
        self.assertEqual(12, tbr.find_start_of_packet_marker())

    def test_find_start_of_packet_marker_no_marker(self):
        tbr = TuningBufferReader('mmmmbbbccde')
        with self.assertRaises(TuningBufferReaderNoStartPacketError):
            tbr.find_start_of_packet_marker()

    def test_find_start_of_packet_marker_sample_1(self):
        tbr = TuningBufferReader('mjqjpqmgbljsphdztnvjfqwrcgsmlb')
        self.assertEqual(7, tbr.find_start_of_packet_marker())

    def test_find_start_of_packet_marker_sample_2(self):
        tbr = TuningBufferReader('bvwbjplbgvbhsrlpgdmjqwftvncz')
        self.assertEqual(5, tbr.find_start_of_packet_marker())

    def test_find_start_of_packet_marker_sample_3(self):
        tbr = TuningBufferReader('nppdvjthqldpwncqszvftbrmjlhg')
        self.assertEqual(6, tbr.find_start_of_packet_marker())

    def test_find_start_of_packet_marker_sample_4(self):
        tbr = TuningBufferReader('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg')
        self.assertEqual(10, tbr.find_start_of_packet_marker())

    def test_find_start_of_packet_marker_sample_5(self):
        tbr = TuningBufferReader('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw')
        self.assertEqual(11, tbr.find_start_of_packet_marker())

    def test_find_start_of_message_marker_sample_1(self):
        tbr = TuningBufferReader('mjqjpqmgbljsphdztnvjfqwrcgsmlb')
        self.assertEqual(19, tbr.find_start_of_message_marker())

    def test_find_start_of_message_marker_sample_2(self):
        tbr = TuningBufferReader('bvwbjplbgvbhsrlpgdmjqwftvncz')
        self.assertEqual(23, tbr.find_start_of_message_marker())

    def test_find_start_of_message_marker_sample_3(self):
        tbr = TuningBufferReader('nppdvjthqldpwncqszvftbrmjlhg')
        self.assertEqual(23, tbr.find_start_of_message_marker())

    def test_find_start_of_message_marker_sample_4(self):
        tbr = TuningBufferReader('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg')
        self.assertEqual(29, tbr.find_start_of_message_marker())

    def test_find_start_of_message_marker_sample_5(self):
        tbr = TuningBufferReader('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw')
        self.assertEqual(26, tbr.find_start_of_message_marker())

