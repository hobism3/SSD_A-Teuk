from commands.base import Command
from shell_constants import LBA_RANGE
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre
from shell_logger import Logger


class WriteCommand(Command):
    def __init__(self, logger: Logger, prefix=Pre.WRITE):
        super().__init__(logger, prefix)

    def parse(self, args: list[str]) -> list[str]:
        if len(args) != 2:
            raise ValueError(Msg.WRITE_HELP)
        lba, data = args
        if not self._check_lba(lba):
            raise ValueError(
                f'LBA must be an integer between {LBA_RANGE[0]} and {LBA_RANGE[-1]}'
            )
        if not self._check_data(data):
            raise ValueError('Data must be a hex string like 0x0129ABCF')
        return ['W', lba, data]

    def parse_result(self, result) -> str:
        if not result:
            return Msg.DONE
        return Msg.ERROR
