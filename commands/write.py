from commands.base import Command
from shell_tool.shell_constants import LBA_RANGE
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class WriteCommand(Command):
    expected_num_args = 2
    help_msg = Msg.WRITE_HELP
    command = 'W'

    def __init__(self, logger: Logger, prefix=Pre.WRITE):
        super().__init__(logger, prefix)
        self._lba = None
        self._data = None
        self._validators = [self._check_lba, self._check_data]

    def _parse(self, args: list[str]) -> list[str]:
        args = args or []
        self._check_argument_count(args)
        self._lba, self._data = args
        self._check_lba(self._lba)
        self._check_data(self._data)
        return [self.command] + args

    def _parse_result(self, result) -> str:
        return Msg.DONE if not result.strip() else Msg.ERROR
