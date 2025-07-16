from commands.base import Command
from commands.read import ReadCommand
from shell_constants import (
    LBA_RANGE,
)
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre
from shell_logger import Logger


class FullReadCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.FULLREAD)
        self._lba = None
        self._read = ReadCommand()

    def parse(self, args: list[str]) -> list[str]:
        if len(args) != 0:
            raise ValueError(Msg.READ_HELP)
        if not self._check_lba(self._lba):
            raise ValueError(
                f'LBA must be an integer between {LBA_RANGE[0]} and {LBA_RANGE[-1]}'
            )
        return ['R', self._lba]

    def execute(self, args) -> bool:
        try:
            self._logger.info('')
            for index in LBA_RANGE:
                args = [str(index)]
                self._read.execute(args)
            return True
        except ValueError:
            self._logger.error(Msg.ERROR)

    def parse_result(self, result) -> str:
        return f'LBA {self._lba}: {result}'
