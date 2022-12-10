from sys import stdin

from src.Rope import Rope, PlanckKnot
from src.UniquePositionObserver import UniquePositionObserver

if __name__ == '__main__':
    rope = Rope()
    tail_observer = UniquePositionObserver()
    for i in range(9):
        if i < 8:
            rope.add_connection(PlanckKnot())
        else:
            rope.add_connection(PlanckKnot([tail_observer]))

    for line in stdin:
        rope.apply_head_movement(line)

    print(f'The tail visited {tail_observer.unique_position_count()} positions at least once')
