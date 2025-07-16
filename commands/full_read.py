import subprocess

from commands.base import Command
from logger import Logger
from shell_constants import (
    LBA_RANGE,
    RUN_SSD,
    SSD_OUTPUT_FILE,
)
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class FullReadCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.READ)
        self._lba = None

    def parse(self, args: list[str]) -> list[str]:
        if len(args) != 0:
            raise ValueError(Msg.READ_HELP)
        if not self._check_lba(self._lba):
            raise ValueError(
                f'LBA must be an integer between {LBA_RANGE[0]} and {LBA_RANGE[-1]}'
            )
        return ['R', self._lba]

    def execute(self, args) -> bool:
        try:
            self._logger.info(Pre.FULLREAD)
            for index in LBA_RANGE:
                self._lba = f'{index:02d}'
                ssd_args = self.parse(args)
                return_code = subprocess.run(RUN_SSD + ssd_args, check=True)
                if return_code.returncode != 0:
                    self._logger.error(Msg.ERROR)
                with open(SSD_OUTPUT_FILE) as f:
                    result = self.parse_result(f.read().strip())
                self._logger.info(result)
        except ValueError:
            self._logger.error(Msg.ERROR)
        return True

    def parse_result(self, result) -> str:
        return f'LBA {self._lba}: {result}'
