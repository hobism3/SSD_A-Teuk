from abc import ABC, abstractmethod
import subprocess

from logger import Logger
from shell_constants import LBA_RANGE, RUN_SSD, SSD_OUTPUT_FILE, Hex, ShellMsg


class Command(ABC):
    _logger = None

    @abstractmethod
    def parse(self, args: list[str]) -> list[str]:
        raise NotImplementedError

    @staticmethod
    def _check_lba(lba):
        if lba.isdigit() and int(lba) in LBA_RANGE:
            return True
        return False

    @staticmethod
    def _check_data(data):
        if (
            data.startswith(Hex.PREFIX)
            and len(data) == Hex.LENGTH
            and all(c in Hex.RANGE for c in data[2:])
        ):
            return True
        return False

    def execute(self, args) -> bool:
        try:
            ssd_args = self.parse(args)
            return_code = subprocess.run(RUN_SSD + ssd_args, check=True)
            if return_code.returncode != 0:
                self._logger.error(ShellMsg.ERROR)
            with open(SSD_OUTPUT_FILE) as f:
                result = self.parse_result(f.read().strip())
            self._logger.info(result)
        except ValueError:
            self._logger.error(ShellMsg.ERROR)
        return True

    @abstractmethod
    def parse_result(self, result) -> str:
        raise NotImplementedError


class ExitCommand(Command):
    def parse(self, args: list[str]) -> list[str]:
        return []

    def execute(self, args, ssd=None) -> bool:
        return False

    def parse_result(self, result) -> str:
        return ''


class HelpCommand(Command):
    def __init__(self):
        self._logger = Logger()

    def parse(self, args: list[str]) -> list[str]:
        return []

    def execute(self, args, sdd=None) -> bool:
        self._logger.info(ShellMsg.HELP)
        return True

    def parse_result(self, result) -> str:
        return ''
