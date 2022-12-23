import unittest
from day14_regolith_reservoir.src.CaveGridWithSand import CaveGridWithSand


class TestCaveGridWithSand(unittest.TestCase):
    def test_sample_input(self):
        cave = CaveGridWithSand()
        fo = open('../sample_input.txt', 'r')
        lines = fo.readlines()
        cave.parse_cave_scan(lines)
        fo.close()
        grains = cave.bring_on_the_sand()
        print(cave.prettify())
        self.assertEqual(24, grains)

    def test_parse_cave_scan_full(self):
        cave = CaveGridWithSand()
        fo = open('../input.txt', 'r')
        lines = fo.readlines()
        cave.parse_cave_scan(lines)
        fo.close()
        grains = cave.bring_on_the_sand()
        print(cave.prettify())
        print(f'There were {grains} units of sand')

    def test_sample_input_with_floor(self):
        cave = CaveGridWithSand()
        fo = open('../sample_input.txt', 'r')
        lines = fo.readlines()
        cave.parse_cave_scan(lines)
        fo.close()
        grains = cave.bring_on_the_sand_with_floor()
        print(cave.prettify())
        self.assertEqual(93, grains)

    def test_parse_cave_scan_full_with_floor(self):
        cave = CaveGridWithSand()
        fo = open('../input.txt', 'r')
        lines = fo.readlines()
        cave.parse_cave_scan(lines)
        fo.close()
        grains = cave.bring_on_the_sand_with_floor()
        print(cave.prettify())
        print(f'There were {grains} units of sand')


if __name__ == '__main__':
    unittest.main()
