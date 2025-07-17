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

    def parse(self, args: list[str]) -> str:
        if len(args) != 1:
            raise ValueError(Msg.FULLWRITE_HELP)
        data = args[0]
        if not self._check_data(data):
            raise ValueError('Data must be a hex string like 0x0129ABCF')
        return data

    def parse_result(self, result) -> str:
        if not result:
            return Msg.DONE
        return Msg.ERROR

    def execute(self, args) -> bool:
        try:
            write_data = self.parse(args)
            for index in LBA_RANGE:
                self._execute_write(index, write_data)
            self._logger.info(Msg.DONE)
            return True
        except ValueError:
            self._logger.error(Msg.ERROR)

    def _execute_write(self, lba, current_value):
        cmd = f'{lba} {current_value}'
        self._write.execute(cmd.split())
