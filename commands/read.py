from commands.base import Command
from shell_constants import LBA_RANGE
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre
from shell_logger import Logger


class ReadCommand(Command):
    def __init__(self, logger: Logger, prefix=Pre.READ):
        super().__init__(logger, prefix)
        self._lba = None

    def parse(self, args: list[str]) -> list[str]:
        if len(args) != 1:
            raise ValueError(Msg.READ_HELP)
        self._lba = args[0]
        if not self._check_lba(self._lba):
            raise ValueError(
                f'LBA must be an integer between {LBA_RANGE[0]} and {LBA_RANGE[-1]}'
            )
        return ['R', self._lba]

    def parse_result(self, result) -> str:
        return f'LBA {self._lba}: {result}'
