from unittest import TestCase

from ..src.FileSystem import File, Directory


class TestFileSystem(TestCase):
    def test_add_and_pretty_print(self):
        dir_e = Directory('e')
        self.assertEqual('e', dir_e.path())
        dir_e.add_child(File('i', 584))
        dir_a = Directory('a')
        dir_a.add_child(dir_e)
        self.assertEqual(dir_e, dir_a.get_sub_directory('e'))
        self.assertEqual('a/e', dir_e.path())
        dir_a.add_child(File('f', 29116))
        dir_a.add_child(File('g', 2557))
        dir_a.add_child(File('h.lst', 62596))
        dir_d = Directory('d')
        dir_d.add_child(File('j', 4060174))
        dir_d.add_child(File('d.log', 8033020))
        dir_d.add_child(File('d.ext', 5626152))
        dir_d.add_child(File('k', 7214296))
        dir_root = Directory('/')
        dir_root.add_child(dir_a)
        dir_root.add_child(File('b.txt', 14848514))
        dir_root.add_child(File('c.dat', 8504156))
        dir_root.add_child(dir_d)

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
            dir_root.to_pretty_string_depth_first()
        )
