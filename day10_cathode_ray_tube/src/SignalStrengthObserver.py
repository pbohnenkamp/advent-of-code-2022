class SignalStrengthObserver:
    def __init__(self) -> None:
        self._signal_strength_sum = 0
        self._cycle_count = 0

    def during_cycle_event(self, register_x_value: int):
        self._cycle_count += 1
        if self._cycle_count == 20 or (self._cycle_count > 40 and ((self._cycle_count - 20) % 40) == 0):
            self._signal_strength_sum += self._cycle_count * register_x_value
            print(
                f'At cycle {self._cycle_count} signal strength is {self._cycle_count * register_x_value} for a total sum of {self._signal_strength_sum}')

    def signal_strength_sum(self):
        return self._signal_strength_sum
