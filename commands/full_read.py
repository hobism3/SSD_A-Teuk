from commands.base import Command
from commands.read import ReadCommand
from logger import Logger
from shell_constants import (
    LBA_RANGE,
)
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class FullReadCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.FULLREAD)
        self._lba = None
        self._read = ReadCommand()

    def parse(self, args: list[str]) -> list[str]:
        if len(args) != 0:
            raise ValueError(Msg.FULLREAD_HELP)

    def execute(self, args) -> bool:
        try:
            self.parse(args)
            self._logger.info('')
            for index in LBA_RANGE:
                args = [str(index)]
                self._read.execute(args)
            return True
        except ValueError:
            self._logger.error(Msg.ERROR)

    def parse_result(self, result) -> str: ...
