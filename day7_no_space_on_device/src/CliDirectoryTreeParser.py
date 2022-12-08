from typing import Iterable, List

from .FileSystem import File, Directory, DIRECTORY_TYPE_KEY

COMMAND_PROMPT = '$'
CHANGE_DIR_COMMAND = 'cd'
PARENT_DIR_KEY = '..'
LIST_COMMAND = 'ls'


class CliDirectoryTreeParser:
    _current_command: str = None
    _root_directory: Directory = None
    _current_directory: Directory = None

    def __init__(self, cli_input: Iterable) -> None:
        self._cli_input = cli_input

    def parse(self):
        for cli_line in self._cli_input:
            split_command = [s.strip() for s in cli_line.split(' ')]
            if self._is_command(split_command):
                self._current_command = self._parse_command(split_command)

            self._handle_command(split_command)
        return self._root_directory

    @staticmethod
    def _is_command(split_command: List[str]):
        return split_command[0] == COMMAND_PROMPT

    @staticmethod
    def _parse_command(split_command: List[str]):
        return split_command[1]

    def _handle_command(self, split_command):
        if self._current_command == CHANGE_DIR_COMMAND:
            self._handle_change_dir(split_command[2])
        elif self._current_command == LIST_COMMAND:
            self._handle_listing(split_command)

    def _handle_change_dir(self, directory_name):
        if directory_name == PARENT_DIR_KEY:
            self._current_directory = self._current_directory.parent()
        elif self._root_directory is None:
            self._root_directory = Directory(directory_name)
            self._current_directory = self._root_directory
        else:
            self._current_directory = self._current_directory.get_sub_directory(directory_name)

    def _handle_listing(self, split_command):
        if self._is_command(split_command):
            pass  # first line is just the command
        elif self._is_directory_type(split_command):
            self._current_directory.add_child(Directory(split_command[1]))
        else:
            self._current_directory.add_child(File(split_command[1], int(split_command[0])))

    @staticmethod
    def _is_directory_type(split_command):
        return split_command[0] == DIRECTORY_TYPE_KEY
