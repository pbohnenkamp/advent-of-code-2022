from sys import stdin


class SectionAssignment:
    def __init__(self, assignment_entry):
        s_min, s_max = assignment_entry.split('-')
        self._min = int(s_min)
        self._max = int(s_max)

    def min(self):
        return self._min

    def max(self):
        return self._max

    def contains(self, other_assignment):
        return self.min() <= other_assignment.min() and self.max() >= other_assignment.max()

    def overlaps(self, other_assignment):
        return not self.max() < other_assignment.min() and not self.min() > other_assignment.max()


def parse_section_assignments(pair_entries):
    entry_1, entry_2 = pair_entries.split(',')
    return SectionAssignment(entry_1), SectionAssignment(entry_2)


if __name__ == '__main__':
    containing_count = 0
    overlapping_count = 0
    for line in stdin:
        section_assignments = parse_section_assignments(line)
        if section_assignments[0].contains(section_assignments[1]) or section_assignments[1].contains(section_assignments[0]):
            containing_count += 1
        if section_assignments[0].overlaps(section_assignments[1]):
            overlapping_count += 1

    print(containing_count)
    print(overlapping_count)
