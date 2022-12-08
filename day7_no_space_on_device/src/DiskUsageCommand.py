from .FileSystem import Directory, FileSystemItem, DIRECTORY_TYPE_KEY


class DiskUsageCommand:
    def __init__(self, directory: Directory) -> None:
        self._directory = directory

    def as_list(self):
        list = [(self._directory.size(), self._directory.path())]
        for child in self._directory.children():
            if self._is_directory(child):
                list += DiskUsageCommand(child).as_list()
        return list

    @staticmethod
    def _is_directory(child: FileSystemItem):
        return child.type() == DIRECTORY_TYPE_KEY
