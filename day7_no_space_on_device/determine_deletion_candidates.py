from sys import stdin

from src.CliDirectoryTreeParser import CliDirectoryTreeParser
from src.DiskUsageCommand import DiskUsageCommand

if __name__ == '__main__':
    root_dir = CliDirectoryTreeParser(stdin).parse()
    print(root_dir.to_pretty_string_depth_first())
    directory_size_list = DiskUsageCommand(root_dir).as_list()

    total_used_space = root_dir.size()
    sum_dirs_under_threshold = 0
    unused_space = 70000000 - total_used_space
    space_to_free_up = 30000000 - unused_space
    current_dir_choice_size = total_used_space
    for size, name in directory_size_list:
        if size <= 100000:
            print(f'Directory {name} included with size of {size}')
            sum_dirs_under_threshold += size

    for size, name in directory_size_list:
        if space_to_free_up <= size < current_dir_choice_size:
            print(f'Directory {name} is with size {size} became the current deletion candidate')
            current_dir_choice_size = size

    print(f'Total size sum of directories under threshold: {sum_dirs_under_threshold}')
    print(
        f'Total size on disk is {total_used_space} leaving {unused_space} in unused space which means we have to free up at least {space_to_free_up}')
    print(f'Total size of smallest directory to delete to free up enough space: {current_dir_choice_size}')
