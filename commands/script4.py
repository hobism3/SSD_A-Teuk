import random

from commands.base import Command
from commands.erase import EraseCommand
from commands.write import WriteCommand
from logger import Logger
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class EraseAndWriteAging(Command):
    def __init__(self):
        self._logger = Logger(Pre.SCRIPT_4)
        self._lba = None
        self._erase = EraseCommand()
        self._write = WriteCommand()

    def parse(self, args: list[str]) -> list[str]:
        if args:
            raise ValueError(Msg.SCRIPT_4_HELP)
        self._lba = 0

    def get_lba_and_size_to_erase(self) -> list[str]:
        size_lba = min(2, 100 - self._lba)
        return [str(self._lba), str(size_lba)]

    def execute(self, args) -> bool:
        try:
            self._execute_erase()
            for _ in range(30):
                for _ in range(49):
                    for _ in range(2):
                        self._execute_write(str(self._lba))
                    self._execute_erase()
                self._logger.info(Msg.PASS)
            return True
        except ValueError:
            self._logger.error(Msg.ERROR)

    def get_random_hex_string(self):
        return f'0x{random.randint(0x00000000, 0xFFFFFFFF):08X}'

    def _execute_erase(self):
        ssd_args = self.get_lba_and_size_to_erase()
        self._erase.execute(ssd_args)
        self._lba += 2

    def _execute_write(self, lba):
        hex_string = self.get_random_hex_string()
        cmd = f'{lba} {hex_string}'
        self._write.execute(cmd.split())

    def parse_result(self, result) -> str: ...
