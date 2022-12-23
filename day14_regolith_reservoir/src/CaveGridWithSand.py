from typing import Iterable


class CaveGridWithSand:

    def __init__(self) -> None:
        self._rocks: set[(int, int)] = set()
        self._sand: set[(int, int)] = set()
        self._has_floor = False

    def parse_cave_scan(self, lines: Iterable[str]):
        for line in lines:
            paths = self._parse_string_paths(line.strip().split(' -> '))
            self._add_rock_paths(paths)
        self._calc_min_max()

    def bring_on_the_sand(self):
        grains_counter = 0
        has_flowed_out_bottom = False
        while not has_flowed_out_bottom:
            is_grain_at_rest = False
            current_grain_position = (500, 0)
            self._sand.add(current_grain_position)
            while not is_grain_at_rest and not has_flowed_out_bottom:
                new_grain_position = self._calc_grain_drop(current_grain_position)
                if current_grain_position != new_grain_position and new_grain_position[1] < self._max_y:
                    self._sand.remove(current_grain_position)
                    self._sand.add(new_grain_position)
                    current_grain_position = new_grain_position
                elif new_grain_position[1] >= self._max_y:
                    self._sand.remove(current_grain_position)
                    has_flowed_out_bottom = True
                else:
                    is_grain_at_rest = True
                    grains_counter += 1
        return grains_counter

    def bring_on_the_sand_with_floor(self):
        self._has_floor = True
        grains_counter = 0
        is_source_blocked = False
        while not is_source_blocked:
            is_grain_at_rest = False
            current_grain_position = (500, 0)
            self._sand.add(current_grain_position)
            while not is_grain_at_rest and not is_source_blocked:
                new_grain_position = self._calc_grain_drop_with_floor(current_grain_position)
                if current_grain_position != new_grain_position:
                    self._sand.remove(current_grain_position)
                    self._sand.add(new_grain_position)
                    current_grain_position = new_grain_position
                    self._recalc_min_max_x(current_grain_position)
                elif new_grain_position == (500, 0):
                    grains_counter += 1
                    is_source_blocked = True
                else:
                    is_grain_at_rest = True
                    grains_counter += 1
        return grains_counter

    def prettify(self):
        max_y = self._max_y + 1 if self._has_floor else self._max_y
        str_grid = ''
        for y in range(max_y + 1):
            for x in range(self._min_x - 2, self._max_x + 3):
                if (x, y) in self._rocks:
                    str_grid += '#'
                elif (x, y) in self._sand:
                    str_grid += 'o'
                else:
                    str_grid += '.'
            str_grid += '\n'
        if self._has_floor:
            str_grid += ''.ljust(self._max_x + 5 - self._min_x, '#')
        else:
            str_grid += ''.ljust(self._max_x + 5 - self._min_x, '.')
        return str_grid

    def _add_rock_paths(self, paths: list[(int, int)]):
        for i in range(len(paths) - 1):
            start_of_path = paths[i]
            end_of_path = paths[i+1]
            if self._path_is_vertical(start_of_path, end_of_path):
                self._draw_vertical_path(start_of_path, end_of_path)
            else:
                self._draw_horizontal_path(start_of_path, end_of_path)

    @staticmethod
    def _parse_string_paths(str_paths: list[str]):
        paths = []
        for str_path in str_paths:
            [str_x, str_y] = str_path.split(',')
            paths.append((int(str_x), int(str_y)))
        return paths

    @staticmethod
    def _path_is_vertical(start_of_path: (int, int), end_of_path: (int, int)):
        return start_of_path[0] == end_of_path[0]

    def _draw_vertical_path(self, start_of_path: (int, int), end_of_path: (int, int)):
        # want to always count up
        y_start = start_of_path[1]
        y_end = end_of_path[1]
        if y_start > y_end:
            y_start = end_of_path[1]
            y_end = start_of_path[1]
        for i in range(y_start, y_end + 1):
            self._rocks.add((start_of_path[0], i))

    def _draw_horizontal_path(self, start_of_path: (int, int),  end_of_path: (int, int)):
        # want to always count up
        x_start = start_of_path[0]
        x_end = end_of_path[0]
        if x_start > x_end:
            x_start = end_of_path[0]
            x_end = start_of_path[0]
        for i in range(x_start, x_end + 1):
            self._rocks.add((i, start_of_path[1]))

    def _calc_min_max(self):
        self._min_x = 9999999
        self._max_x = 0
        self._max_y = 0
        for rock in self._rocks:
            if rock[0] > self._max_x:
                self._max_x = rock[0]
            if rock[0] < self._min_x:
                self._min_x = rock[0]
            if rock[1] > self._max_y:
                self._max_y = rock[1]

    def _calc_grain_drop(self, current_grain_position):
        if not self._below_blocked(current_grain_position):
            return current_grain_position[0], current_grain_position[1] + 1
        elif not self._diagonal_left_blocked(current_grain_position):
            return current_grain_position[0] - 1, current_grain_position[1] + 1
        elif not self._diagonal_right_blocked(current_grain_position):
            return current_grain_position[0] + 1, current_grain_position[1] + 1
        else:
            return current_grain_position

    def _below_blocked(self, current_grain_position):
        potential_new_position = (current_grain_position[0], current_grain_position[1] + 1)
        return potential_new_position in self._rocks or potential_new_position in self._sand

    def _diagonal_left_blocked(self, current_grain_position):
        potential_new_position = (current_grain_position[0] - 1, current_grain_position[1] + 1)
        return potential_new_position in self._rocks or potential_new_position in self._sand

    def _diagonal_right_blocked(self, current_grain_position):
        potential_new_position = (current_grain_position[0] + 1, current_grain_position[1] + 1)
        return potential_new_position in self._rocks or potential_new_position in self._sand

    def _calc_grain_drop_with_floor(self, current_grain_position):
        if self._is_grain_on_floor(current_grain_position):
            return current_grain_position
        else:
            return self._calc_grain_drop(current_grain_position)

    def _is_grain_on_floor(self, current_grain_position):
        return current_grain_position[1] + 1 == self._max_y + 2

    def _recalc_min_max_x(self, current_grain_position):
        if current_grain_position[0] > self._max_x:
            self._max_x = current_grain_position[0]
        elif current_grain_position[0] < self._min_x:
            self._min_x = current_grain_position[0]

            
