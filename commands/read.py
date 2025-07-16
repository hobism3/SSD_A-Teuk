import subprocess
from subprocess import CalledProcessError

from commands.base import Command
from shell_constants import LBA_RANGE, RUN_SSD, SSD_OUTPUT_FILE
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre
from shell_logger import Logger


class ReadCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.READ)
        self._lba = None

    def parse(self, args: list[str]) -> list[str]:
        if len(args) != 1:
            raise ValueError(Msg.READ_HELP)
        self._lba = args[0]
        if not self._check_lba(self._lba):
            raise ValueError(
                f'LBA must be an integer between {LBA_RANGE[0]} and {LBA_RANGE[-1]}'
            )
        return ['R', self._lba]

    def parse_result(self, result) -> str:
        return f'LBA {self._lba}: {result}'

    def execute(self, args: list[str]) -> str:
        try:
            ssd_args = self.parse(args)
            return_code = subprocess.run(RUN_SSD + ssd_args, check=True)
            if return_code.returncode != 0:
                self._logger.error(Msg.ERROR)
            with open(SSD_OUTPUT_FILE) as f:
                read_value = f.read().strip()
                result = self.parse_result(read_value)
            self._logger.info(result)
            return read_value
        except (ValueError, CalledProcessError):
            self._logger.error(Msg.ERROR)
