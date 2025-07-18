from commands.base import Command
from commands.validator import Validator, check_lba
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
        self._validators: list[Validator] = [Validator(check_lba, (0,))]

    def _parse(self, args):
        parsed_args = super()._parse(args)
        self._lba = args[0]
        return parsed_args

    def _parse_result(self, result) -> str:
        return f'LBA {int(self._lba):02}: {result}'
