from dataclasses import dataclass, field
from sys import maxsize


def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)


class Sensor:

    def __init__(self, sensor_point, beacon_point) -> None:
        super().__init__()

        self.sensor_point: (int, int) = sensor_point
        self.beacon_point: (int, int) = beacon_point
        self.beacon_taxicab_distance: int = self._calc_taxicab_distance(sensor_point, beacon_point)

    def get_taxicab_distance_to_beacon(self):
        return self._calc_taxicab_distance(self.sensor_point, self.beacon_point)

    def is_beacon_prohibited_at_point(self, point: (int, int)):
        return self.beacon_point != point and self._is_within_beacon_taxicab_distance(point)

    def sensor_coverage_report(self, point: (int, int)):
        return self._is_within_beacon_taxicab_distance(point), self.beacon_point == point, self.sensor_point == point,\
               self._calc_max_covered_x_for_line(point)

    def _is_within_beacon_taxicab_distance(self, point):
        point_taxicab_dist = self._calc_taxicab_distance(self.sensor_point, point)
        return point_taxicab_dist <= self.beacon_taxicab_distance

    @staticmethod
    def _calc_taxicab_distance(point_a, point_b):
        return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])

    def _calc_max_covered_x_for_line(self, line_point):
        mid_point_of_line = self.sensor_point[0], line_point[1]
        taxicab_distance_to_mid = self._calc_taxicab_distance(self.sensor_point, mid_point_of_line)
        return mid_point_of_line[0] + (self.beacon_taxicab_distance - taxicab_distance_to_mid)


class BeaconGrid:
    def __init__(self) -> None:
        self._sensors: list[Sensor] = []
        self._min_x = maxsize
        self._max_x = -maxsize-1
        self._max_y = 0
        self._beacon_points: set[(int, int)] = set()
        self._sensor_points: set[(int, int)] = set()

    @property
    def max_x(self):
        return self._max_x

    @property
    def min_x(self):
        return self._min_x

    @property
    def max_y(self):
        return self._max_y

    @property
    def sensors(self):
        return self._sensors.copy()

    def parse_sensor_data(self, lines: list[str]):
        for line in lines:
            [sensor_input, beacon_input] = self._cut_unneeded_input(line)
            self.append_sensor(Sensor(self._input_to_point(sensor_input), self._input_to_point(beacon_input)))

    @staticmethod
    def _cut_unneeded_input(line):
        line = line.strip()
        [sensor_input, beacon_input] = line[len('Sensor at '):].split(':')
        beacon_input = beacon_input[len(' closest beacon is at '):]
        return sensor_input, beacon_input

    @staticmethod
    def _input_to_point(sensor_input: str):
        [x_input, y_input] = sensor_input.split(',')
        x_input = x_input[len('x='):]
        y_input = y_input.strip()[len('y='):]
        return int(x_input), int(y_input)

    def append_sensor(self, sensor: Sensor):
        if sensor.sensor_point[0] + sensor.get_taxicab_distance_to_beacon() > self._max_x:
            self._max_x = sensor.sensor_point[0] + sensor.get_taxicab_distance_to_beacon()
        if sensor.sensor_point[0] - sensor.get_taxicab_distance_to_beacon() < self._min_x:
            self._min_x = sensor.sensor_point[0] - sensor.get_taxicab_distance_to_beacon()
        if sensor.sensor_point[1] + sensor.get_taxicab_distance_to_beacon() > self._max_y:
            self._max_y = sensor.sensor_point[1] + sensor.get_taxicab_distance_to_beacon()
        self._sensors.append(sensor)
        self._sensor_points.add(sensor.sensor_point)
        self._beacon_points.add(sensor.beacon_point)

    def points_excluded_at_line(self, y: int):
        count_points = 0
        for i in range(self._min_x, self._max_x):
            if self._is_beacon_prohibited_at_point((i, y)):
                count_points += 1
        return count_points

    def detect_distress_beacon(self, max_grid: int):
        beacon_frequency = 0
        for y in range(max_grid):
            x = 0
            while x < max_grid:
                sensor_report = self._find_first_sensor_report_covering_point((x, y))
                if sensor_report is None:
                    # found our point!
                    beacon_frequency = x * 4000000 + y
                    break
                else:
                    x = sensor_report[3] + 1
            if beacon_frequency > 0:
                break
        return beacon_frequency

    def _is_beacon_prohibited_at_point(self, point: (int, int)):
        return point in self._sensor_points\
                or first_true(self._sensors, False, lambda sensor: sensor.is_beacon_prohibited_at_point((point[0], point[1])))

    def _find_first_sensor_report_covering_point(self, point: (int, int)):
        for sensor in self._sensors:
            sensor_report = sensor.sensor_coverage_report(point)
            if sensor_report[0]:
                return sensor_report
        return None

    