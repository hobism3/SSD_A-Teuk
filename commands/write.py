from commands.base import Command
from commands.validator import Validator, check_data, check_lba
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
        self._validators: list[Validator] = [
            Validator(check_lba, (0,)),
            Validator(check_data, (1,)),
        ]

    def _parse_result(self, result) -> str:
        return Msg.DONE if not result.strip() else Msg.ERROR
