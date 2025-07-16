import random
import subprocess

from commands.base import Command
from commands.read import ReadCommand
from commands.write import WriteCommand
from logger import Logger
from shell_constants import RUN_SSD, ShellMsg
from shell_constants import ShellPrefix as Pre


class PartialLBAWriteCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.SCRIPT2)
        self._lba = None
        self._read = ReadCommand()
        self._write = WriteCommand()
        self._random_value = random.randint(0x00000000, 0xFFFFFFFF)

    def parse(self, args: list[str]) -> list[str]: ...

    def execute(self, args) -> bool:
        try:
            sample_index = ['4', '0', '3', '1', '2']

            for _ in range(30):
                hex_string = f'0x{self._random_value:08X}'
                for index in sample_index:
                    self._lba = index
                    ssd_args = ['W', self._lba, hex_string]
                    return_code = subprocess.run(RUN_SSD + ssd_args, check=True)
                    if return_code.returncode != 0:
                        self._logger.error(ShellMsg.ERROR)

                for index in sample_index:
                    ssd_args = [index]
                    read_value = self._read.execute(ssd_args)
                    if read_value != hex_string:
                        if read_value != hex_string:
                            self._logger.info(Pre.SCRIPT2 + ShellMsg.FAIL)
                            return True
                self._logger.info(Pre.SCRIPT2 + ShellMsg.PASS)

        except ValueError:
            self._logger.error(ShellMsg.ERROR)
        return True

    def parse_result(self, result) -> str: ...
