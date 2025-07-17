from commands.script import ScriptCommand
from shell_constants import (
    LBA_RANGE,
)
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre
from shell_logger import Logger


class FullReadCommand(ScriptCommand):
    def __init__(self, logger: Logger, prefix=Pre.FULLREAD):
        super().__init__(logger, prefix)
        self._lba = None

    def execute(self, args=None) -> bool:
        try:
            self._logger.print_blank_line()
            self._logger.print_and_log(self._prefix)
            for index in LBA_RANGE:
                self.read(index)
        except ValueError:
            self._logger.print_and_log(self._prefix, Msg.ERROR)
        return True

    def parse(self, args: list[str]) -> list[str]:
        return args

    def parse_result(self, result) -> str:
        return result
