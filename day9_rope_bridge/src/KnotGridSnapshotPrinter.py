from .Rope import Rope, PlanckKnot


class KnotGridSnapshotPrinter:
    def __init__(self, rope: Rope) -> None:
        self._rope = rope
        self._start_planck_knot = PlanckKnot()

    def print_current_grid(self):
        knots_by_id = self._get_knots_by_id()
        width, height, x_axis_scaling_factor, y_axis_scaling_factor = self._calc_grid_dimensions(knots_by_id)
        grid = ''
        for y in range(height + 1):
            grid_line = ''
            for x in range(width + 1):
                rope_id = self._find_knot_at_position(knots_by_id, x + x_axis_scaling_factor, y + y_axis_scaling_factor)
                if rope_id is None:
                    grid_line += '.'
                else:
                    grid_line += rope_id
            grid = grid_line + '\n' + grid

        return grid

    def _get_knots_by_id(self):
        knots_by_id: dict[str, PlanckKnot] = dict()
        knots_by_id['H'] = self._rope.get_head_knot()
        for i, planck_knot in enumerate(self._rope.get_connected_knots()):
            knots_by_id[str(i + 1)] = planck_knot
        knots_by_id['s'] = self._start_planck_knot
        return knots_by_id

    @staticmethod
    def _calc_grid_dimensions(knots_by_id):
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for planck_knot in knots_by_id.values():
            if planck_knot.get_position()[0] > max_x:
                max_x = planck_knot.get_position()[0]
            if planck_knot.get_position()[0] < min_x:
                min_x = planck_knot.get_position()[0]
            if planck_knot.get_position()[1] > max_y:
                max_y = planck_knot.get_position()[1]
            if planck_knot.get_position()[1] < min_y:
                min_y = planck_knot.get_position()[1]
        x_scaling_factor = min_x if min_x < 0 else 0
        y_scaling_factor = min_y if min_y < 0 else 0
        return max_x - min_x, max_y - min_y, x_scaling_factor, y_scaling_factor

    @staticmethod
    def _find_knot_at_position(knots_by_id, x, y):
        for knot_id, knot in knots_by_id.items():
            if knot.get_position() == (x, y):
                return knot_id
        return None
