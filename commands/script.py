from commands.base import Command
from commands.read import ReadCommand
from commands.write import WriteCommand
from shell_constants import ShellMsg
from shell_logger import Logger


class ScriptCommand(Command):
    def __init__(self, logger: Logger, prefix=None):
        super().__init__(logger, prefix)
        self._commands = []
        self._read_cmd: ReadCommand | None = None
        self._write_cmd: WriteCommand | None = None

    @property
    def read_cmd(self):
        if self._read_cmd is None:
            self._read_cmd = ReadCommand(self._logger, prefix=None)
        return self._read_cmd

    @property
    def write_cmd(self):
        if self._write_cmd is None:
            self._write_cmd = WriteCommand(self._logger, prefix=None)
        return self._write_cmd

    def read(self, lba) -> str:
        if not isinstance(lba, str):
            lba = str(lba)
        self.read_cmd.execute([lba])
        return self.read_cmd.result

    def write(self, lba, value):
        if not isinstance(lba, str):
            lba = str(lba)
        if not isinstance(value, str):
            value = str(value)
        self.write_cmd.execute([lba, value])

    def read_with_verify(self, lba, expected) -> bool:
        read_value = self.read(lba)
        if read_value != expected:
            self._logger.print_and_log(self._prefix, ShellMsg.FAIL)
            return False
        return True

    def parse(self, args: list[str]) -> list[str]:
        return []

    def parse_result(self, result) -> str:
        return ''
