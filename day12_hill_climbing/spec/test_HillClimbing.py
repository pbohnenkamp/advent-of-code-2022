from unittest import TestCase

from day12_hill_climbing.src.HeightmapParser import HeightmapParser, Heightmap


class TestHeightmap(TestCase):
    def test_sample_optimally(self):
        fo = open('../sample_input.txt', 'r')
        lines = fo.readlines()
        parser = HeightmapParser()
        heightmap = parser.parse(lines)
        fo.close()
        path = heightmap.find_optimal_path()
        self.assertEqual(31, len(path) - 1)

    def test_input(self):
        fo = open('../input.txt', 'r')
        lines = fo.readlines()
        parser = HeightmapParser()
        heightmap = parser.parse(lines)
        fo.close()

        print(f'The map is {heightmap.get_map_width()} nodes wide')
        print(f'The map is {heightmap.get_map_height()} nodes high')

        path = heightmap.find_optimal_path()
        print(f'The optimal method returns {len(path) - 1}')
        self.assertEqual(504, len(path) - 1)
        print_path(heightmap, path)

    def test_input_to_nearest_a(self):
        fo = open('../input.txt', 'r')
        lines = fo.readlines()
        parser = HeightmapParser()
        heightmap = parser.parse(lines)
        fo.close()

        print(f'The map is {heightmap.get_map_width()} nodes wide')
        print(f'The map is {heightmap.get_map_height()} nodes high')

        path = heightmap.find_optimal_path(True)
        print(f'The optimal method returns {len(path) - 1}')
        self.assertEqual(500, len(path) - 1)
        print_path(heightmap, path)


def print_path(hmap: Heightmap, path):
    print_grid = []
    for y in range(hmap.get_map_height()):
        grid_line = []
        for x in range(hmap.get_map_width()):
            grid_line.append(hmap._map[y][x].height)
        print_grid.append(grid_line)

    for node in path:
        print_grid[node.y][node.x] = print_grid[node.y][node.x].upper()

    for line in print_grid:
        str_line = ''
        for char in line:
            str_line += char
        print(str_line)
