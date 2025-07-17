import subprocess

from commands.base import Command
from shell_constants import LBA_RANGE, RUN_SSD, SIZE_RANGE, SSD_OUTPUT_FILE
from shell_constants import ShellMsg
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre
from shell_logger import Logger


class EraseCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.ERASE)

    def execute(self, args: list[str]) -> bool:
        try:
            erase_cmd, current_lba, remaining = self._parse_erase_args(args)
            self._execute_chunk_erase(erase_cmd, current_lba, remaining)
            self._check_output_file()
        except ValueError:
            self._logger.error(ShellMsg.ERROR)
        return True

    def _check_output_file(self):
        with open(SSD_OUTPUT_FILE) as f:
            result = self.parse_result(f.read().strip())
        self._logger.info(result)

    def _execute_chunk_erase(
        self, erase_cmd: str, current_lba: int, remaining: int
    ) -> None:
        while remaining > 0:
            chunk_size = min(10, remaining)
            full_cmd = RUN_SSD + [erase_cmd] + [str(current_lba), str(chunk_size)]
            return_code = subprocess.run(full_cmd, check=True)
            if return_code.returncode != 0:
                self._logger.error(ShellMsg.ERROR)
                break
            current_lba += chunk_size
            remaining -= chunk_size

    def _parse_erase_args(self, args: list[str]) -> tuple[str, int, int]:
        ssd_args = self.parse(args)
        return ssd_args[0], int(ssd_args[1]), int(ssd_args[2])

    def parse(self, args: list[str]) -> list[str]:
        if len(args) != 2:
            raise ValueError(Msg.ERASE_HELP)
        lba, size = args
        self._check_validity(lba, size)

        return ['E', lba, size]

    def parse_result(self, result) -> str:
        if not result:
            return Msg.DONE
        return Msg.ERROR

    def _check_validity(self, lba, size):
        if not self._check_lba(lba):
            raise ValueError(
                f'LBA must be an integer between {LBA_RANGE[0]} and {LBA_RANGE[-1]}'
            )
        if not self._check_size(size):
            raise ValueError(
                f'Size must be an integer between {SIZE_RANGE[0]} and {SIZE_RANGE[-1]}'
            )
        if not self._check_end_lba(lba, size):
            raise ValueError(
                f'End LBA must not exceed the maximum value of {LBA_RANGE[-1]}'
            )

    @staticmethod
    def _check_size(size):
        if size.isdigit() and int(size) in SIZE_RANGE:
            return True
        return False

    @staticmethod
    def _check_end_lba(lba, size):
        if int(lba) + int(size) - 1 <= 99:
            return True
        return False
