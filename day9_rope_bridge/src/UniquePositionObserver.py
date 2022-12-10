class UniquePositionObserver:
    def __init__(self) -> None:
        self._tail_positions = set()

    def notify(self, position):
        self._tail_positions.add(position)

    def unique_position_count(self):
        return len(self._tail_positions)
