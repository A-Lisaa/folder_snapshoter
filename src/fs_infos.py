from __future__ import annotations

import os
from abc import ABC
from dataclasses import dataclass
from os import DirEntry, PathLike

from .interfaces import ICompressable


@dataclass
class Info(ABC, ICompressable):
    name: str
    # unix time
    created_time: int


@dataclass
class FileInfo(Info):
    # size of the file in bytes
    size: int
    # unix time
    accessed_time: int
    changed_time: int

    @classmethod
    def from_dir_entry(cls, entry: DirEntry):
        stat = entry.stat()
        return cls(
            name=entry.name,
            size=stat.st_size,
            accessed_time=int(stat.st_atime),
            created_time=int(stat.st_ctime),
            changed_time=int(stat.st_mtime)
        )

    @classmethod
    def from_compressed_json(cls, compressed_json: list):
        return cls(*compressed_json)

    def to_compressed_json(self) -> list:
        return [
            self.name,
            self.size,
            self.accessed_time,
            self.created_time,
            self.changed_time
        ]


@dataclass
class FolderInfo(Info):
    @classmethod
    def from_dir_entry(cls, entry: DirEntry):
        stat = entry.stat()
        return cls(
            name=entry.name,
            created_time=int(stat.st_ctime)
        )

    @classmethod
    def from_path(cls, path: str | PathLike):
        stat = os.stat(path)
        return cls(
            name=os.path.split(os.path.realpath(path))[1],
            created_time=int(stat.st_ctime)
        )

    @classmethod
    def from_compressed_json(cls, compressed_json: list):
        return cls(*compressed_json)

    def to_compressed_json(self) -> list:
        return [
            self.name,
            self.created_time
        ]
