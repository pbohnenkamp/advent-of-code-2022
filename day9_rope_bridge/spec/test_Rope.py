from unittest import TestCase
from unittest.mock import MagicMock, call

from day9_rope_bridge.src.KnotGridSnapshotPrinter import KnotGridSnapshotPrinter
from day9_rope_bridge.src.Rope import Rope, PlanckKnot
from day9_rope_bridge.src.UniquePositionObserver import UniquePositionObserver


class TestEventListener:
    def notify(self, *args, **kwargs):
        pass


class TestRope(TestCase):
    def test_apply_head_movement_to_single_connection(self):
        test_event_listener = TestEventListener()
        test_event_listener.notify = MagicMock()
        tail_knot = PlanckKnot([test_event_listener])
        rope = Rope()
        rope.add_connection(tail_knot)
        # Should send tail notify for start position
        test_event_listener.notify.assert_called_once_with((0, 0))
        test_event_listener.notify.reset_mock()

        # Move up - tail should not move
        rope.apply_head_movement('U 1')
        self.assertEqual((0, 1), rope.get_head_knot().get_position())
        self.assertEqual((0, 0), tail_knot.get_position())
        test_event_listener.notify.assert_not_called()
        test_event_listener.notify.reset_mock()

        # Move up again - tail should move up 1
        rope.apply_head_movement('U 1')
        self.assertEqual((0, 2), rope.get_head_knot().get_position())
        self.assertEqual((0, 1), tail_knot.get_position())
        test_event_listener.notify.assert_called_once_with((0, 1))
        test_event_listener.notify.reset_mock()

        # Move up multiple times - tail should move up 2 times
        rope.apply_head_movement('U 2')
        self.assertEqual((0, 4), rope.get_head_knot().get_position())
        self.assertEqual((0, 3), tail_knot.get_position())
        test_event_listener.notify.assert_has_calls([call((0, 2)), call((0, 3))])
        test_event_listener.notify.reset_mock()

        # Move left 1 spot - tail should not move
        rope.apply_head_movement('L 1')
        self.assertEqual((-1, 4), rope.get_head_knot().get_position())
        self.assertEqual((0, 3), tail_knot.get_position())
        test_event_listener.notify.assert_not_called()
        test_event_listener.notify.reset_mock()

        # Move left 1 more spot - tail should move diagonal to catch up
        rope.apply_head_movement('L 1')
        self.assertEqual((-2, 4), rope.get_head_knot().get_position())
        self.assertEqual((-1, 4), tail_knot.get_position())
        test_event_listener.notify.assert_called_once_with((-1, 4))
        test_event_listener.notify.reset_mock()

        # Move left multiple times - tail should move left to catch up
        rope.apply_head_movement('L 2')
        self.assertEqual((-4, 4), rope.get_head_knot().get_position())
        self.assertEqual((-3, 4), tail_knot.get_position())
        test_event_listener.notify.assert_has_calls([call((-2, 4)), call((-3, 4))])
        test_event_listener.notify.reset_mock()

        # Move down multiple times - tail should move down to catch up
        rope.apply_head_movement('D 4')
        self.assertEqual((-4, 0), rope.get_head_knot().get_position())
        self.assertEqual((-4, 1), tail_knot.get_position())
        test_event_listener.notify.assert_has_calls([call((-4, 3)), call((-4, 2)), call((-4, 1))])
        test_event_listener.notify.reset_mock()

        # Move right multiple times - tail should move right to catch up
        rope.apply_head_movement('R 4')
        self.assertEqual((0, 0), rope.get_head_knot().get_position())
        self.assertEqual((-1, 0), tail_knot.get_position())
        test_event_listener.notify.assert_has_calls([call((-3, 0)), call((-2, 0)), call((-1, 0))])
        test_event_listener.notify.reset_mock()

        # Move head back over tail
        rope.apply_head_movement('L 1')
        self.assertEqual((-1, 0), rope.get_head_knot().get_position())
        self.assertEqual((-1, 0), tail_knot.get_position())
        test_event_listener.notify.assert_not_called()
        test_event_listener.notify.reset_mock()

    def test_step_through_example(self):
        rope = Rope()
        printer = KnotGridSnapshotPrinter(rope)
        for i in range(9):
            rope.add_connection(PlanckKnot())
        print(printer.print_current_grid())

        rope.apply_head_movement('R 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('R 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('R 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('R 1')
        print(printer.print_current_grid())

        rope.apply_head_movement('U 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('U 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('U 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('U 1')
        print(printer.print_current_grid())

        rope.apply_head_movement('L 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('L 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('L 1')
        print(printer.print_current_grid())

        rope.apply_head_movement('D 1')
        print(printer.print_current_grid())

        rope.apply_head_movement('R 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('R 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('R 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('R 1')
        print(printer.print_current_grid())

        rope.apply_head_movement('D 1')
        print(printer.print_current_grid())

        rope.apply_head_movement('L 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('L 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('L 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('L 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('L 1')
        print(printer.print_current_grid())

        rope.apply_head_movement('R 1')
        print(printer.print_current_grid())
        rope.apply_head_movement('R 1')
        print(printer.print_current_grid())

    def test_larger_example(self):
        rope = Rope()
        printer = KnotGridSnapshotPrinter(rope)
        tail_observer = UniquePositionObserver()
        for i in range(9):
            if i < 8:
                rope.add_connection(PlanckKnot())
            else:
                rope.add_connection(PlanckKnot([tail_observer]))
        print(printer.print_current_grid())

        rope.apply_head_movement('R 5')
        print(printer.print_current_grid())

        rope.apply_head_movement('U 8')
        print(printer.print_current_grid())

        rope.apply_head_movement('L 8')
        print(printer.print_current_grid())

        rope.apply_head_movement('D 3')
        print(printer.print_current_grid())

        rope.apply_head_movement('R 17')
        print(printer.print_current_grid())

        rope.apply_head_movement('D 10')
        print(printer.print_current_grid())

        rope.apply_head_movement('L 25')
        print(printer.print_current_grid())

        rope.apply_head_movement('U 20')
        print(printer.print_current_grid())

        print(tail_observer.unique_position_count())
