import subprocess

from commands.base import Command
from shell_tool.shell_constants import LBA_RANGE, RUN_SSD, SIZE_RANGE, SSD_OUTPUT_FILE
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
    
    def _parse(self, args: list[str]) -> list[str]:
        args = args or []
        self._check_argument_count(args)

        lba, size = args[0], args[1]
        self._check_lba(lba)
        self._check_size(size)
        self._check_boundary(lba, size)

        self._lba = int(lba)
        self._size = int(size)
        return [self.command] + args
    
    def _parse_result(self, result: str) -> str:
        return Msg.DONE if not result.strip() else Msg.ERROR

    def execute(self, args: list[str] = None) -> bool:
        try:
            parsed_args = self._parse(args)
            self._execute_chunks(self._lba, self._size, self._chunk_size)
            self._process_result()
        except (ValueError, subprocess.CalledProcessError):
            self._logger.print_and_log(self._prefix, Msg.ERROR)
        return True

    def _check_size(self, size: str) -> bool:
        if size.isdigit() and int(size) in SIZE_RANGE:
            return True
        raise ValueError(f"Invalid size: {size}")

    def _check_boundary(self, lba: str, size: str) -> bool:
        if int(lba) + int(size) - 1 <= max(LBA_RANGE):
            return True
        raise ValueError("Erase range exceeds device limit.")
