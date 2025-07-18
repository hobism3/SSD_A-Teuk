from commands.base import Command, command_handler
from commands.mixin import WriteSupportMixin
from commands.validator import Validator
from shell_tool.shell_constants import LBA_RANGE
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class FullWriteCommand(WriteSupportMixin, Command):
    expected_num_args = 1
    help_msg = Msg.FULLWRITE_HELP

    def __init__(self, logger: Logger, prefix=Pre.FULLWRITE):
        super().__init__(logger, prefix)
        self._validators: list[Validator] = [Validator(self._check_data, (0,))]

    @command_handler
    def execute(self, args=None) -> bool:
        self._parse(args)
        for lba in LBA_RANGE:
            self.write(lba, args[0], True)
        self._logger.print_and_log(self._prefix, Msg.DONE)
        return True
