import random

from commands.base import Command
from commands.read import ReadCommand
from commands.write import WriteCommand
from logger import Logger
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class PartialLBAWriteCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.SCRIPT2)
        self._lba = None
        self._read = ReadCommand()
        self._write = WriteCommand()
        self._random_value = random.randint(0x00000000, 0xFFFFFFFF)

    def parse(self, args: list[str]) -> None:
        if len(args) != 0:
            raise ValueError(Msg.SCRIPT_2_HELP)

    def parse_result(self, result) -> str: ...

    def execute(self, args: list[str]) -> bool:
        try:
            self.parse(args)
            sample_index = ['4', '0', '3', '1', '2']

            for _ in range(30):
                hex_string = f'0x{self._random_value:08X}'
                for index in sample_index:
                    self._execute_write(index, hex_string)

                for index in sample_index:
                    ssd_args = [index]
                    read_value = self._read.execute(ssd_args)
                    if read_value != hex_string:
                        if read_value != hex_string:
                            self._logger.info(Msg.FAIL)
                            return True
                self._logger.info(Msg.PASS)
            return True
        except ValueError:
            self._logger.error(Msg.ERROR)

    def _execute_write(self, lba, current_value):
        cmd = f'{lba} {current_value}'
        self._write.execute(cmd.split())
