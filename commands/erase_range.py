from subprocess import CalledProcessError

from commands.base import Command
from commands.mixin import EraseSupportMixin
from commands.validator import Validator
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class EraseRangeCommand(EraseSupportMixin, Command):
    expected_num_args = 2
    help_msg = Msg.ERASE_RANGE_HELP

    def __init__(self, logger: Logger, prefix=Pre.ERASERANGE):
        super().__init__(logger, prefix)
        self._validators: list[Validator] = [
            Validator(self._check_lba, (0,)),
            Validator(self._check_lba, (1,)),
            Validator(self._check_lba_range, (0, 1)),
        ]

    def execute(self, args: list[str]) -> bool:
        try:
            parsed_args = self._parse(args)
            self.erase_range(*parsed_args[1:])
            self._logger.print_and_log(self._prefix, Msg.DONE)
        except ValueError:
            self._logger.print(message=self.help_msg)
        except CalledProcessError:
            self._logger.print_and_log(self._prefix, Msg.ERROR)
        return True
