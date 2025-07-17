import subprocess

from commands.base import Command
from commands.validator import Validator
from shell_tool.shell_constants import LBA_RANGE, SIZE_RANGE
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class EraseCommand(Command):
    expected_num_args = 2
    help_msg = Msg.ERASE_HELP
    command = 'E'

    def __init__(self, logger: Logger, prefix=Pre.ERASE):
        super().__init__(logger, prefix)
        self._chunk_size = 10
        self._validators: list[Validator] = [
            Validator(self._check_lba, (0,)),
            Validator(self._check_size, (1,)),
            Validator(self._check_boundary, (0, 1)),
        ]

    def _parse_result(self, result: str) -> str:
        return Msg.DONE if not result.strip() else Msg.ERROR

    def execute(self, args: list[str] = None) -> bool:
        try:
            self._parse(args)
            self._execute_chunks(self._lba, self._size, self._chunk_size)
            self._process_result()
        except (ValueError, subprocess.CalledProcessError):
            self._logger.print_and_log(self._prefix, Msg.ERROR)
        return True

    def _check_size(self, size: str) -> bool:
        if size.isdigit() and int(size) in SIZE_RANGE:
            return True
        raise ValueError(f'Invalid size: {size}')

    def _check_boundary(self, lba: str, size: str) -> bool:
        if int(lba) + int(size) - 1 <= max(LBA_RANGE):
            return True
        raise ValueError('Erase range exceeds device limit.')
