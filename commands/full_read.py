from commands.base import Command
from commands.mixin import ReadSupportMixin
from shell_tool.shell_constants import LBA_RANGE
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class FullReadCommand(ReadSupportMixin, Command):
    expected_num_args = 0
    help_msg = Msg.FULLREAD_HELP

    def __init__(self, logger: Logger, prefix=Pre.FULLREAD):
        super().__init__(logger, prefix)

    def execute(self, args=None) -> bool:
        try:
            self._parse(args)
            self._logger.print_and_log(self._prefix)
            for index in LBA_RANGE:
                self.read(index)
            self._logger.print_and_log(self._prefix, Msg.DONE)
        except ValueError:
            self._logger.print_and_log(self._prefix, Msg.ERROR)
        return True

    def _parse(self, args: list[str]) -> list[str]:
        return args
