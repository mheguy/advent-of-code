from __future__ import annotations

import re
from dataclasses import dataclass, field

from advent_of_code.shared.utils import run_solution

FS_SPACE = 70000000
SPACE_NEEDED = 30000000


@dataclass
class File:
    name: str
    size: int


@dataclass
class Folder:
    name: str
    parent: Folder | None
    files: list[File] = field(default_factory=list)
    sub_folders: dict[str, Folder] = field(default_factory=dict)
    _size: int | None = None

    @property
    def size(self):
        if self._size is None:
            self._size = self.get_size()

        return self._size

    def add_file(self, file: File) -> None:
        self.files.append(file)

    def add_folder(self, name: str, folder: Folder) -> None:
        self.sub_folders[name] = folder

    def get_size(self) -> int:
        size = sum(folder.get_size() for folder in self.sub_folders.values())
        size += sum(file.size for file in self.files)
        return size


@dataclass
class CommandBlock:
    command_name: str
    output_lines: list[str]


class Terminal:
    def __init__(self):
        self.root = Folder("/", None)
        self.cwd = self.root

    def process_command_block(self, command_block: CommandBlock) -> None:
        name = command_block.command_name
        name = name.removeprefix("$ ")
        if name.startswith("ls"):
            self.list(command_block)
        elif name.startswith("cd"):
            self.chdir(name.removeprefix("cd "))

    def chdir(self, target: str) -> None:
        if target == ".." and self.cwd.parent:
            self.cwd = self.cwd.parent
        elif target == "/":
            self.cwd = self.root
        else:
            self.cwd = self.cwd.sub_folders[target]

    def list(self, command_block: CommandBlock) -> None:
        for line in command_block.output_lines:
            if line.startswith("dir"):
                name = line.removeprefix("dir ")
                self.cwd.add_folder(name, Folder(name, self.cwd))
            else:
                result = re.search(r"(\d+) (.+)", line)
                if not result:
                    raise ValueError

                self.cwd.add_file(File(result[2], int(result[1])))


def parse_text_input(text_lines: list[str]) -> list[CommandBlock]:
    commands_and_outputs = []
    new_item = []
    for line in text_lines:
        if line.startswith("$"):
            commands_and_outputs.append(new_item)
            new_item = []

        new_item.append(line)
    commands_and_outputs.append(new_item)

    command_blocks = []
    for c_and_o in commands_and_outputs:
        if not c_and_o:
            continue
        if len(c_and_o) == 1:
            command_blocks.append(CommandBlock(c_and_o[0], []))
        else:
            command_blocks.append(CommandBlock(c_and_o[0], c_and_o[1:]))

    return command_blocks


def get_all_folders(folder: Folder) -> list[Folder]:
    folders = [folder]
    for sub_folder in folder.sub_folders.values():
        folders.extend(get_all_folders(sub_folder))

    return folders


def get_puzzle_answer(folders: list[Folder]) -> int:
    total = 0
    for folder in folders:
        print(f"{folder.name} - {folder.size}")
        if folder.size <= 100000:  # noqa: PLR2004
            total += folder.size
    return total


def get_space_needed(root: Folder) -> int:
    used_space = root.get_size()
    free_space = FS_SPACE - used_space
    return SPACE_NEEDED - free_space


def get_smallest_viable_folder(folders: list[Folder], minimum_size: int) -> Folder:
    viable_folders = (folder for folder in folders if folder.size >= minimum_size)
    return min(
        viable_folders,
        key=lambda x: x.get_size(),
    )


def main(lines: list[str]) -> None:
    command_blocks = parse_text_input(lines)
    terminal = Terminal()

    for command_block in command_blocks:
        terminal.process_command_block(command_block)

    folders = get_all_folders(terminal.root)
    puzzle_answer = get_puzzle_answer(folders)
    print(puzzle_answer)

    folder = get_smallest_viable_folder(get_all_folders(terminal.root), get_space_needed(terminal.root))
    print(f"{folder.name} - {folder.size}")


if __name__ == "__main__":
    run_solution("2022", "dec_07", main)
