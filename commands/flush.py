from subprocess import CalledProcessError

from commands.base import Command
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class FlushCommand(Command):
    def __init__(self, logger: Logger, prefix=Pre.FLUSH):
        super().__init__(logger, prefix)
        self._command = 'F'

    def parse(self, args: list[str]) -> list[str]:
        if args:
            raise ValueError(Msg.FLUSH_HELP)
        return [self._command]

    def parse_result(self, result: int) -> str:
        if result == 0:
            return Msg.DONE
        return Msg.ERROR

    def execute(self, args: list[str]) -> bool:
        try:
            ssd_args = self.parse(args)
            self._run_sdd(ssd_args)
        except (ValueError, CalledProcessError):
            self._logger.print_and_log(self._prefix, Msg.ERROR)
        self._logger.print_and_log(self._prefix, Msg.DONE)
        return True
