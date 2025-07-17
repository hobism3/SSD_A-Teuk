import subprocess
from subprocess import CalledProcessError

from commands.base import Command
from logger import Logger
from shell_constants import RUN_SSD
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class FlushCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.FLUSH)

    def parse(self, args: list[str]) -> list[str]:
        if args:
            raise ValueError(Msg.FLUSH_HELP)
        return ['E']

    def parse_result(self, result: int) -> str:
        if result == 0:
            return Msg.DONE
        return Msg.ERROR

    def execute(self, args: list[str]) -> bool:
        try:
            ssd_args = self.parse(args)
            return_code = subprocess.run(RUN_SSD + ssd_args, check=True)
            result = self.parse_result(return_code.returncode)
            self._logger.info(result)
            return True
        except (ValueError, CalledProcessError):
            self._logger.error(Msg.ERROR)
