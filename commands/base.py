from abc import ABC, abstractmethod
import subprocess
from subprocess import CalledProcessError

from shell_constants import LBA_RANGE, RUN_SSD, SSD_OUTPUT_FILE, Hex, ShellMsg
from shell_logger import Logger


class Command(ABC):
    def __init__(self, logger: Logger, prefix=None):
        self._logger = logger
        self.result = None
        self._prefix = prefix

    @abstractmethod
    def parse(self, args: list[str]) -> list[str]:
        raise NotImplementedError

    @staticmethod
    def _check_lba(lba: str) -> bool:
        if lba.isdigit() and int(lba) in LBA_RANGE:
            return True
        raise ValueError

    @staticmethod
    def _check_data(data: str) -> bool:
        if (
            data.startswith(Hex.PREFIX)
            and len(data) == Hex.LENGTH
            and all(c in Hex.RANGE for c in data[2:])
        ):
            return True
        raise ValueError

    def execute(self, args: list[str] = None) -> bool:
        try:
            ssd_args = self.parse(args)
            subprocess.run(RUN_SSD + ssd_args, check=True)
            with open(SSD_OUTPUT_FILE) as f:
                self.result = f.read().strip()
                self._logger.print_and_log(self._prefix, self.parse_result(self.result))
        except (ValueError, CalledProcessError):
            self._logger.print_and_log(self._prefix, ShellMsg.ERROR)
        return True

    @abstractmethod
    def parse_result(self, result: str) -> str:
        raise NotImplementedError


class ExitCommand(Command):
    def parse(self, args: list[str]) -> list[str]:
        return []

    def execute(self, args: list[str] = None) -> bool:
        return False

    def parse_result(self, result) -> str:
        return ''


class HelpCommand(Command):
    def parse(self, args: list[str]) -> list[str]:
        return []

    def execute(self, args: list[str] = None) -> bool:
        self._logger.print(self._prefix, self.parse_result())
        return True

    def parse_result(self, result=None) -> str:
        return ShellMsg.HELP
