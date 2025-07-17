import random

from commands.base import Command
from commands.read import ReadCommand
from commands.write import WriteCommand
from shell_constants import ShellMsg
from shell_constants import ShellPrefix as Pre
from shell_logger import Logger


class PartialLBAWriteCommand(Command):
    def __init__(self, logger: Logger, prefix=Pre.SCRIPT2):
        super().__init__(logger, prefix)
        self._lba = None
        self._read = ReadCommand(self._logger, prefix=None)
        self._write = WriteCommand(self._logger, prefix=None)
        self._random_value = random.randint(0x00000000, 0xFFFFFFFF)

    def parse(self, args: list[str]) -> list[str]: ...

    def execute(self, args=None) -> bool:
        try:
            sample_index = ['4', '0', '3', '1', '2']
            self._logger.print_blank_line()
            self._logger.print_and_log(self._prefix, None)
            for _ in range(30):
                hex_string = f'0x{self._random_value:08X}'
                for index in sample_index:
                    self._execute_write(index, hex_string)

                for index in sample_index:
                    ssd_args = [index]
                    self._read.execute(ssd_args)
                    read_value = self._read.result
                    if read_value != hex_string:
                        if read_value != hex_string:
                            self._logger.print_and_log(self._prefix, ShellMsg.FAIL)
                            return True
                self._logger.print_and_log(self._prefix, ShellMsg.PASS)
        except ValueError:
            self._logger.print_and_log(self._prefix, ShellMsg.ERROR)
        return True

    def _execute_write(self, lba, current_value):
        cmd = f'{lba} {current_value}'
        self._write.execute(cmd.split())

    def parse_result(self, result) -> str: ...
