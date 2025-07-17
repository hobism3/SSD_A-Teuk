from commands.base import Command
from commands.validator import Validator
from commands.mixin import WriteSupportMixin
from shell_tool.shell_constants import LBA_RANGE
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class FullWriteCommand(WriteSupportMixin, Command):
    expected_num_args = 1
    help_msg = Msg.FULLWRITE_HELP

    def __init__(self, logger: Logger, prefix=Pre.FULLWRITE):
        super().__init__(logger, prefix)
        self._validators: list[Validator] = [
            Validator(self._check_data, (0,))
        ]

    def execute(self, args=None) -> bool:
        try:
            self._parse(args)
            self.logger_verbose = False
            for lba in LBA_RANGE:
                self.write(lba, args[0], True)
            self._logger.print_and_log(self._prefix, Msg.DONE)
        except ValueError:
            self._logger.print_and_log(self._prefix, Msg.ERROR)
        return True
