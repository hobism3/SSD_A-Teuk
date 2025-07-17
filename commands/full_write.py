from commands.base import Command
from commands.write import WriteCommand
from shell_constants import LBA_RANGE
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre
from shell_logger import Logger


class FullWriteCommand(Command):
    def __init__(self, logger: Logger, prefix=Pre.FULLWRITE):
        super().__init__(logger, prefix)
        self._lba = None
        self._write = WriteCommand(self._logger, prefix=None)

    def execute(self, args=None) -> bool:
        try:
            for index in LBA_RANGE:
                self._execute_write(index, args[0])
                self._logger.print_and_log(self._prefix, Msg.DONE)
        except ValueError:
            self._logger.print_and_log(self._prefix, Msg.ERROR)
        return True

    def _execute_write(self, lba, current_value):
        args = [str(lba), current_value]
        self._write.execute(args)

    def parse(self, args: list[str]) -> list[str]:
        return args

    def parse_result(self, result) -> str:
        return result
