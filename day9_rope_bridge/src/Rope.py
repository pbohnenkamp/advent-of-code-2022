from math import copysign


class PlanckKnot:
    def __init__(self, event_subscribers=None) -> None:
        if event_subscribers is None:
            event_subscribers = []
        self._event_subscribers = event_subscribers
        self._position = (0, 0)
        self._emit_change_event()

    def set_position(self, position: (int, int)):
        if not self._position == position:
            self._assert_valid_new_position(position)
            self._position = position
            self._emit_change_event()

    def _assert_valid_new_position(self, position: (int, int)):
        if abs(self._position[0] - position[0]) > 1 or abs(self._position[1] - position[1]) > 1:
            raise Exception(
                f'The new position cannot be more than one value away from either axis, start: {repr(self._position)} to: {repr(position)}')

    def _emit_change_event(self):
        for subscriber in self._event_subscribers:
            subscriber.notify(self.get_position())

    def get_position(self):
        return self._position


class Rope:
    def __init__(self, head_knot: PlanckKnot = None) -> None:
        if head_knot is None:
            head_knot = PlanckKnot()
        self._head_knot = head_knot
        self._connected_knots = []

    def apply_head_movement(self, movement_input: str):
        direction, planck_lengths = movement_input.strip().split(' ')
        for tick in range(int(planck_lengths)):
            self._move_head(direction)

    def _move_head(self, direction):
        if direction == 'U':
            self._move_head_up()
        elif direction == 'L':
            self._move_head_left()
        elif direction == 'D':
            self._move_head_down()
        elif direction == 'R':
            self._move_head_right()
        self._reposition_connections()

    def _move_head_up(self):
        self._head_knot.set_position((self._head_knot.get_position()[0], self._head_knot.get_position()[1] + 1))

    def _move_head_left(self):
        self._head_knot.set_position((self._head_knot.get_position()[0] - 1, self._head_knot.get_position()[1]))

    def _move_head_down(self):
        self._head_knot.set_position((self._head_knot.get_position()[0], self._head_knot.get_position()[1] - 1))

    def _move_head_right(self):
        self._head_knot.set_position((self._head_knot.get_position()[0] + 1, self._head_knot.get_position()[1]))

    def _reposition_connections(self):
        previous_knot = self._head_knot
        for planckKnot in self._connected_knots:
            self._reposition_knot(planckKnot, previous_knot.get_position())
            previous_knot = planckKnot

    @staticmethod
    def _reposition_knot(planck_knot: PlanckKnot, connected_position: (int, int)):
        new_x = planck_knot.get_position()[0]  # assume no movement to start
        new_y = planck_knot.get_position()[1]  # assume no movement to start
        if (abs(connected_position[0] - planck_knot.get_position()[0]) > 1
            and abs(connected_position[1] - planck_knot.get_position()[1]) >= 1) \
                or (abs(connected_position[1] - planck_knot.get_position()[1]) > 1
                    and abs(connected_position[0] - planck_knot.get_position()[0]) >= 1):
            # need to move both axis (diagonal)
            new_x = planck_knot.get_position()[0] + int(
                copysign(1, connected_position[0] - planck_knot.get_position()[0]))
            new_y = planck_knot.get_position()[1] + int(
                copysign(1, connected_position[1] - planck_knot.get_position()[1]))
        elif abs(connected_position[0] - planck_knot.get_position()[0]) > 1:
            # need to just move the x-axis
            new_x = planck_knot.get_position()[0] + int(
                copysign(1, connected_position[0] - planck_knot.get_position()[0]))
        elif abs(connected_position[1] - planck_knot.get_position()[1]) > 1:
            # need to just move the y-axis
            new_y = planck_knot.get_position()[1] + int(
                copysign(1, connected_position[1] - planck_knot.get_position()[1]))
        if not planck_knot.get_position() == (new_x, new_y):
            planck_knot.set_position((new_x, new_y))

    def add_connection(self, planck_knot: PlanckKnot):
        self._connected_knots.append(planck_knot)

    def get_head_knot(self):
        return self._head_knot

    def get_connected_knots(self):
        return self._connected_knots.copy()
