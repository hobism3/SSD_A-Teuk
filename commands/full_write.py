from commands.base import Command
from commands.write import WriteCommand
from logger import Logger
from shell_constants import LBA_RANGE
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class FullWriteCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.FULLWRITE)
        self._lba = None
        self._write = WriteCommand()

    def parse(self, args: list[str]) -> list[str]: ...

    def execute(self, args) -> bool:
        try:
            for index in LBA_RANGE:
                self._execute_write(index, args[0])
                self._logger.info(Msg.DONE)
            return True
        except ValueError:
            self._logger.error(Msg.ERROR)

    def parse_result(self, result) -> str:
        if not result:
            return Msg.DONE
        return Msg.ERROR

    def _execute_write(self, lba, current_value):
        cmd = f'{lba} {current_value}'
        self._write.execute(cmd.split())
