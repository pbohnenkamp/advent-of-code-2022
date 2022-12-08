from typing import Dict, Union

TAB_SIZE = 2
DIRECTORY_TYPE_KEY = 'dir'
FILE_TYPE_KEY = 'file'


class FileSystemItem:
    _name: str = None
    _size: int = None
    _parent: 'Directory' = None
    _type: str = None

    def type(self):
        return self._type

    def name(self):
        return self._name

    def size(self):
        return self._size

    def parent(self):
        return self._parent

    def set_parent(self, parent: 'Directory'):
        self._parent = parent

    def path(self):
        path = self.name()
        parent = self.parent()
        while parent is not None:
            parent_name = parent.name() if parent.name() == '/' else parent.name() + '/'
            path = parent_name + path
            parent = parent.parent()
        return path

    @staticmethod
    def _get_tab_level_from_kwargs(**kwargs):
        tab_level = 0
        if kwargs.__contains__('tab_level'):
            tab_level = kwargs['tab_level']
        return tab_level

    @staticmethod
    def _get_padding_for_pretty_string(**kwargs):
        tab_level = FileSystemItem._get_tab_level_from_kwargs(**kwargs)
        return "".rjust(TAB_SIZE * tab_level, " ")


class File(FileSystemItem):
    def __init__(self, name: str, size: int) -> None:
        self._name = name
        self._size = size
        self._type = FILE_TYPE_KEY

    def to_pretty_string_depth_first(self, **kwargs):
        padding = self._get_padding_for_pretty_string(**kwargs)
        return f'{padding}- {self.name()} ({FILE_TYPE_KEY}, size={self.size()})\n'


class Directory(FileSystemItem):
    def __init__(self, name: str) -> None:
        self._name = name
        self._size: int = 0
        self._type = DIRECTORY_TYPE_KEY
        self._children: Dict[str, Union[Directory, File]] = dict()

    def to_pretty_string_depth_first(self, **kwargs):
        tab_level = self._get_tab_level_from_kwargs(**kwargs)
        padding = self._get_padding_for_pretty_string(**kwargs)

        pretty_string = f'{padding}- {self.name()} ({DIRECTORY_TYPE_KEY})\n'
        for sub_item in self._children.values():
            pretty_string += sub_item.to_pretty_string_depth_first(tab_level=tab_level + 1)

        return pretty_string

    def add_child(self, child: Union['Directory', File]):
        child.set_parent(self)
        self._children[child.name()] = child

    def children(self):
        return list(self._children.values())

    def size(self):
        total_size = 0
        for child in self._children.values():
            total_size += child.size()
        return total_size

    def get_sub_directory(self, directory_name: str):
        return self._children[directory_name]
