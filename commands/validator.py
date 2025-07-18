from typing import Callable

from shell_tool.shell_constants import LBA_RANGE, SIZE_RANGE, Hex


class Validator:
    def __init__(self, fn: Callable, indexes: tuple[int, ...]):
        self.fn = fn
        self.indexes = indexes

    def validate(self, args: list[str]):
        values = [args[i] for i in self.indexes]
        self.fn(*values)


def check_lba(lba: str):
    if not (lba.isdigit() and int(lba) in LBA_RANGE):
        raise ValueError(f'Invalid LBA: {lba}')


def check_data(data: str):
    if not (
        data.startswith(Hex.PREFIX)
        and len(data) == Hex.LENGTH
        and all(c in Hex.RANGE for c in data[2:])
    ):
        raise ValueError(f'Invalid hex data: {data}')


def check_size(size: str):
    if not (size.isdigit() and int(size) in SIZE_RANGE):
        raise ValueError(f'Invalid size: {size}')


def check_boundary(lba: str, size: str):
    if int(lba) + int(size) - 1 > max(LBA_RANGE):
        raise ValueError(f'Invalid range: lba({lba})+size({size}) > {max(LBA_RANGE)}')


def check_lba_range(start: str, end: str):
    if int(start) > int(end):
        raise ValueError(f'Invalid range: start({start}) > end({end})')
