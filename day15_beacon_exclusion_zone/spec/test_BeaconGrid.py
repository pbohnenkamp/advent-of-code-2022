import unittest
from day15_beacon_exclusion_zone.src.BeaconGrid import BeaconGrid


class TestBeaconGrid(unittest.TestCase):
    def test_sample_input(self):
        beacon_grid = BeaconGrid()
        fo = open('../sample_input.txt', 'r')
        lines = fo.readlines()
        beacon_grid.parse_sensor_data(lines)
        fo.close()
        self.assertEqual(14, len(beacon_grid.sensors))
        self.assertEqual((2, 18), beacon_grid.sensors[0].sensor_point)
        self.assertEqual(7, beacon_grid.sensors[0].get_taxicab_distance_to_beacon())
        self.assertEqual((-2, 15), beacon_grid.sensors[0].beacon_point)
        self.assertEqual((8, 7), beacon_grid.sensors[6].sensor_point)
        self.assertEqual((2, 10), beacon_grid.sensors[6].beacon_point)
        self.assertEqual((20, 1), beacon_grid.sensors[13].sensor_point)
        self.assertEqual((15, 3), beacon_grid.sensors[13].beacon_point)
        self.assertEqual(26, beacon_grid.max_y)
        self.assertEqual(-8, beacon_grid.min_x)
        self.assertEqual(28, beacon_grid.max_x)

        self.assertEqual(26, beacon_grid.points_excluded_at_line(10))
        self.assertEqual(29, beacon_grid.points_excluded_at_line(16))

        self.assertEqual(56000011, beacon_grid.detect_distress_beacon(20))

    def test_input(self):
        beacon_grid = BeaconGrid()
        fo = open('../input.txt', 'r')
        lines = fo.readlines()
        beacon_grid.parse_sensor_data(lines)
        fo.close()
        points_excluded = beacon_grid.points_excluded_at_line(2000000)
        self.assertEqual(26, len(beacon_grid.sensors))
        print(f'Minimum X: {beacon_grid.min_x}')
        print(f'Maximum X: {beacon_grid.max_x}')
        print(f'Maximum Y: {beacon_grid.max_y}')
        print(f'{points_excluded} points cannot be a beacon at line 2000000')
        self.assertEqual(5299855, points_excluded)
        frequency = beacon_grid.detect_distress_beacon(4000000)
        print(f'{frequency} is the frequency of the distress beacon')

if __name__ == '__main__':
    unittest.main()
