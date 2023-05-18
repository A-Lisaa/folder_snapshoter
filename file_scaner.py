from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from os import DirEntry, PathLike


@dataclass
class Info(ABC):
    name: str
    # unix time
    created: float

    @staticmethod
    @abstractmethod
    def from_dir_entry(entry: DirEntry) -> Info:
        ...


@dataclass
class FileInfo(Info):
    # size of the file in bytes
    size: int
    # unix time
    accessed: float
    changed: float

    @staticmethod
    def from_dir_entry(entry: DirEntry) -> FileInfo:
        stat = entry.stat()
        return FileInfo(
            name=entry.name,
            size=stat.st_size,
            accessed=stat.st_atime,
            created=stat.st_ctime,
            changed=stat.st_mtime
        )


@dataclass
class FolderInfo(Info):
    @staticmethod
    def from_dir_entry(entry: DirEntry) -> FolderInfo:
        stat = entry.stat()
        return FolderInfo(
            name=entry.name,
            created=stat.st_ctime
        )

    @staticmethod
    def from_path(path: str | PathLike) -> FolderInfo:
        stat = os.stat(path)
        return FolderInfo(
            name=os.path.split(path)[1],
            created=stat.st_ctime
        )


@dataclass
class FileSystemEntry(ABC):
    info: Info


@dataclass
class File(FileSystemEntry):
    ...


@dataclass
class Folder(FileSystemEntry):
    folders: list[Folder]
    files: list[File]


def scan_folder(folder_path: str | PathLike | DirEntry) -> Folder:
    if isinstance(folder_path, DirEntry):
        info = FolderInfo.from_dir_entry(folder_path)
    else:
        info = FolderInfo.from_path(folder_path)
    folders = []
    files = []
    with os.scandir(folder_path) as directory:
        for entry in directory:
            if entry.is_dir():
                folder = scan_folder(entry)
                folders.append(folder)
            elif entry.is_file():
                file = File(FileInfo.from_dir_entry(entry))
                files.append(file)
    return Folder(info, folders, files)


def main():
    result = scan_folder(".")
    print(json.dumps(asdict(result), indent=4))


if __name__ == "__main__":
    main()
