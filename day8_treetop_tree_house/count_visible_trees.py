from sys import stdin

from src.TreeMapParser import TreeMapParser

if __name__ == '__main__':
    tree_map = TreeMapParser(stdin).parse()
    print(f'Total number of visible trees: {tree_map.count_visible_trees()}')
    print(f'Score for most scenic tree: {tree_map.find_most_scenic_tree()}')
