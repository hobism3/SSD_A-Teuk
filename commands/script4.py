import random

from commands.base import Command
from commands.erase import EraseCommand
from commands.write import WriteCommand
from logger import Logger
from shell_constants import MAX_LBA
from shell_constants import Script as Const
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class EraseAndWriteAging(Command):
    def __init__(self):
        self._logger = Logger(Pre.SCRIPT_4)
        self._lba = 0
        self._erase = EraseCommand()
        self._write = WriteCommand()

    def parse(self, args: list[str]) -> None:
        if args:
            raise ValueError(Msg.SCRIPT_4_HELP)

    def parse_result(self, result) -> str: ...

    def execute(self, args: list[str]) -> bool:
        try:
            self.parse(args)
            self._execute_erase()
            for _ in range(30):
                for _ in range(49):
                    self._execute_write_double()
                    self._execute_erase()
                self._logger.info(Msg.PASS)
            return True
        except ValueError:
            self._logger.error(Msg.ERROR)

    def _execute_write_double(self):
        self._execute_write(str(self._lba))
        self._execute_write(str(self._lba))

    def _execute_erase(self):
        ssd_args = self.get_lba_and_size_to_erase()
        self._erase.execute(ssd_args)
        self._lba += Const.STEP_LBA

    def _execute_write(self, lba: str):
        hex_string = self.get_random_hex_string()
        cmd = f'{lba} {hex_string}'
        self._write.execute(cmd.split())

    def get_random_hex_string(self):
        return f'0x{random.randint(0x00000000, 0xFFFFFFFF):08X}'

    def get_lba_and_size_to_erase(self) -> list[str]:
        size_erase = min(Const.DEFAULT_ERASE_SIZE, MAX_LBA - self._lba + 1)
        return [str(self._lba), str(size_erase)]
