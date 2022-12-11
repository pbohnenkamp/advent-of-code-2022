import unittest
from unittest.mock import MagicMock, call

from day10_cathode_ray_tube.src.ClockCircuit import ClockCircuit
from day10_cathode_ray_tube.src.CrtDrawingObserver import CrtDrawingObserver
from day10_cathode_ray_tube.src.SignalStrengthObserver import SignalStrengthObserver


class TestEventListener:
    def during_cycle_event(self, *args, **kwargs):
        pass


class TestClockCircuit(unittest.TestCase):
    def test_run_program(self):
        test_event_listener = TestEventListener()
        test_event_listener.during_cycle_event = MagicMock()
        clock_circuit = ClockCircuit([test_event_listener])
        clock_circuit.load_instructions([
            'noop',
            'addx 3',
            'addx -5'
        ])
        clock_circuit.run_program()
        test_event_listener.during_cycle_event.assert_has_calls([
            call(1),
            call(1),
            call(1),
            call(4),
            call(4)
        ])

    def test_with_sample_data(self):
        signal_strength_observer = SignalStrengthObserver()
        crt_drawing_observer = CrtDrawingObserver()
        clock_circuit = ClockCircuit([signal_strength_observer, crt_drawing_observer])
        fo = open('../sample_input.txt', 'r')
        lines = fo.readlines()
        clock_circuit.load_instructions(lines)
        fo.close()
        clock_circuit.run_program()
        self.assertEqual(13140, signal_strength_observer.signal_strength_sum())
        self.assertEqual(
            '''##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
''',
            crt_drawing_observer.get_screen_output()
        )


if __name__ == '__main__':
    unittest.main()
