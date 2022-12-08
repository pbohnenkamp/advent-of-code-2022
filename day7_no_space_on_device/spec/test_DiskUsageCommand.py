from unittest import TestCase

from ..src.DiskUsageCommand import DiskUsageCommand
from ..src.FileSystem import Directory, File


class TestDiskUsageCommand(TestCase):
    def test_disk_usage_as_list(self):
        dir_root = Directory('/')
        dir_a = Directory('a')
        dir_d = Directory('d')
        dir_root.add_child(dir_a)
        dir_root.add_child(File('b.txt', 14848514))
        dir_root.add_child(File('c.dat', 8504156))
        dir_root.add_child(dir_d)
        dir_e = Directory('e')
        self.assertListEqual([(0, 'e')], DiskUsageCommand(dir_e).as_list())
        dir_a.add_child(dir_e)
        self.assertListEqual([(0, '/a'), (0, '/a/e')], DiskUsageCommand(dir_a).as_list())
        dir_a.add_child(File('f', 29116))
        dir_a.add_child(File('g', 2557))
        dir_a.add_child(File('h.lst', 62596))
        dir_e.add_child(File('i', 584))
        self.assertListEqual([(584, '/a/e')], DiskUsageCommand(dir_e).as_list())
        self.assertListEqual([(94853, '/a'), (584, '/a/e')], DiskUsageCommand(dir_a).as_list())
        dir_d.add_child(File('j', 4060174))
        dir_d.add_child(File('d.log', 8033020))
        dir_d.add_child(File('d.ext', 5626152))
        dir_d.add_child(File('k', 7214296))
        self.assertListEqual([(24933642, '/d')], DiskUsageCommand(dir_d).as_list())
        self.assertListEqual([(48381165, '/'), (94853, '/a'), (584, '/a/e'), (24933642, '/d')],
                             DiskUsageCommand(dir_root).as_list())
