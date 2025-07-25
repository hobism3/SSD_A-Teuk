from commands.base import Command, command_handler
from commands.mixin import EraseSupportMixin
from commands.validator import Validator, check_lba, check_lba_range
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class EraseRangeCommand(EraseSupportMixin, Command):
    expected_num_args = 2
    help_msg = Msg.ERASE_RANGE_HELP

    def __init__(self, logger: Logger, prefix=Pre.ERASERANGE):
        super().__init__(logger, prefix)
        self._validators: list[Validator] = [
            Validator(check_lba, (0,)),
            Validator(check_lba, (1,)),
            Validator(check_lba_range, (0, 1)),
        ]

    @command_handler
    def execute(self, args: list[str]) -> bool:
        parsed_args = self._parse(args)
        self.erase_range(*parsed_args[1:])
        self._logger.print_and_log(self._prefix, Msg.DONE)
        return True
