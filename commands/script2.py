import random
import subprocess

from commands.base import Command
from commands.read import ReadCommand
from commands.write import WriteCommand
from logger import Logger
from shell_constants import RUN_SSD, SSD_OUTPUT_FILE, ShellMsg
from shell_constants import ShellPrefix as Pre


class PartialLBAWriteCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.READ)
        self._lba = None
        self._read = ReadCommand()
        self._write = WriteCommand()
        self._random_value = random.randint(0x00000000, 0xFFFFFFFF)

    def parse(self, args: list[str]) -> list[str]: ...

    def execute(self, args, ssd=None) -> bool:
        try:
            sample_index = ['04', '00', '03', '01', '02']

            for _ in range(30):
                hex_string = f'0x{self._random_value:08X}'
                for index in sample_index:
                    self._lba = index
                    ssd_args = ['W', self._lba, hex_string]
                    return_code = subprocess.run(RUN_SSD + ssd_args, check=True)
                    if return_code.returncode != 0:
                        self._logger.error(ShellMsg.ERROR)

                for index in sample_index:
                    self._lba = index
                    ssd_args = ['R', self._lba]
                    return_code = subprocess.run(RUN_SSD + ssd_args, check=True)
                    if return_code.returncode != 0:
                        self._logger.error(ShellMsg.ERROR)
                    with open(SSD_OUTPUT_FILE) as f:
                        read_value = f.read().strip()
                        if read_value != hex_string:
                            print('[2_PartialLBAWrite] Fail')
                            return True
                print('[2_PartialLBAWrite] Pass')

        except ValueError:
            self._logger.error(ShellMsg.ERROR)
        return True

    def parse_result(self, result) -> str: ...
