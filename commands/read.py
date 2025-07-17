from commands.base import Command
from shell_tool.shell_constants import LBA_RANGE
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class ReadCommand(Command):
    expected_num_args = 1
    help_msg = Msg.READ_HELP
    command = 'R'

    def __init__(self, logger: Logger, prefix=Pre.READ):
        super().__init__(logger, prefix)
        self._lba = None

    def _parse(self, args: list[str]) -> list[str]:
        args = args or []
        self._check_argument_count(args)
        self._lba = args[0]
        self._check_lba(self._lba)
        return [self.command] + args

    def _parse_result(self, result) -> str:
        return f'LBA {int(self._lba):02}: {result}'
