from unittest import TestCase

from ..src.CliDirectoryTreeParser import CliDirectoryTreeParser


class TestCliDirectoryTreeParser(TestCase):
    def test_parse(self):
        lines = open('day7_no_space_on_device/sample_input.txt', 'r').readlines()
        dir_parser = CliDirectoryTreeParser(lines)
        root_dir = dir_parser.parse()
        self.assertEqual(
            """- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
""",
            root_dir.to_pretty_string_depth_first()
        )
