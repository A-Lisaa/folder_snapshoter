from __future__ import annotations

import os
from os import DirEntry, PathLike

from .fs_entities import File, Folder
from .fs_infos import FileInfo, FolderInfo


def scan_folder(folder_path: str | PathLike[str] | DirEntry) -> Folder:
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
