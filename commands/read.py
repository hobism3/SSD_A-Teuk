from commands.base import Command
from logger import Logger
from shell_constants import LBA_RANGE
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class ReadCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.READ)

    def parse(self, args: list[str]) -> tuple:
        if len(args) != 1:
            raise ValueError(Msg.READ_HELP)
        lba = args[0]
        if not self._check_lba(lba):
            raise ValueError(
                f'LBA must be an integer between {LBA_RANGE[0]} and {LBA_RANGE[-1]}'
            )
        return 'R', lba
