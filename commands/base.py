from abc import ABC, abstractmethod

from logger import Logger
from shell_constants import LBA_RANGE, Hex
from shell_constants import ShellMsg as Msg


class Command(ABC):
    _logger = None

    @abstractmethod
    def parse(self, args: list[str]) -> tuple:
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

    def execute(self, args, ssd) -> bool:
        try:
            ssd_args = self.parse(args)
            ssd.execute(*ssd_args)
            self._logger.info(Msg.DONE)
        except ValueError:
            self._logger.error(Msg.ERROR)
        return True


class ExitCommand(Command):
    def parse(self, args: list[str]) -> tuple:
        return ()

    def execute(self, args, ssd=None) -> bool:
        return False


class HelpCommand(Command):
    def __init__(self):
        self._logger = Logger()

    def parse(self, args: list[str]) -> tuple:
        return ()

    def execute(self, args, sdd=None) -> bool:
        self._logger.info(Msg.HELP)
        return True
