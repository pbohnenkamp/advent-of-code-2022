class CrtDrawingObserver:
    def __init__(self) -> None:
        self._cycle_count = 0
        self._horizontal_drawing_position = 0
        self._crt_output: str = ''

    def during_cycle_event(self, register_x_value: int):
        self._cycle_count += 1
        self._crt_output += '#' if self._is_sprite_active_at_drawing_position(register_x_value) else '.'
        self._horizontal_drawing_position += 1
        if self._cycle_count % 40 == 0:
            self._scroll_down()

    def get_screen_output(self):
        return self._crt_output

    def _is_sprite_active_at_drawing_position(self, register_x_value):
        return register_x_value - 1 <= self._horizontal_drawing_position <= register_x_value + 1

    def _scroll_down(self):
        self._crt_output += '\n'
        self._horizontal_drawing_position = 0
