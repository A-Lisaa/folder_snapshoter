from __future__ import annotations

import json
from abc import ABC
from dataclasses import dataclass
from os import PathLike

import brotli

from .fs_infos import FileInfo, FolderInfo, Info
from .interfaces import ICompressable


@dataclass
class FileSystemEntity(ABC, ICompressable):
    info: Info


@dataclass
class File(FileSystemEntity):
    @classmethod
    def from_compressed_json(cls, compressed_json: list):
        return cls(
            FileInfo.from_compressed_json(compressed_json[0])
        )

    def to_compressed_json(self) -> list:
        return [
            self.info.to_compressed_json()
        ]


@dataclass
class Folder(FileSystemEntity):
    folders: list[Folder]
    files: list[File]

    @classmethod
    def from_compressed_json(cls, compressed_json: list):
        return cls(
            FolderInfo.from_compressed_json(compressed_json[0]),
            [
                Folder.from_compressed_json(compressed_folder)
                for compressed_folder
                in compressed_json[1]
            ],
            [
                File.from_compressed_json(compressed_folder)
                for compressed_folder
                in compressed_json[2]
            ]
        )

    @classmethod
    def from_brotli_archive(cls, brotli_path: str | PathLike):
        with open(f"{brotli_path}.br", "rb") as brotli_file:
            json_string = brotli.decompress(brotli_file.read()).decode()
            json_list = json.loads(json_string)
            return cls.from_compressed_json(json_list)

    def to_compressed_json(self) -> list:
        return [
            self.info.to_compressed_json(),
            [folder.to_compressed_json() for folder in self.folders],
            [file.to_compressed_json() for file in self.files]
        ]

    def to_brotli_archive(self, brotli_path: str | PathLike[str]) -> None:
        json_string = json.dumps(self.to_compressed_json(), separators=(',', ':'))
        with open(f"{brotli_path}.br", "wb") as brotli_file:
            brotli_file.write(brotli.compress(json_string.encode()))
