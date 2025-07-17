import random

from commands.base import Command
from commands.read import ReadCommand
from commands.write import WriteCommand
from logger import Logger
from shell_constants import SCRIPT_3_ROTATE_CNT
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class WriteReadAging(Command):
    def __init__(self):
        self._logger = Logger(Pre.SCRIPT_3)
        self.write_cmd = WriteCommand()
        self.read_cmd = ReadCommand()

    def parse(self, args: list[str]) -> None:
        if len(args) != 0:
            raise ValueError(Msg.SCRIPT_3_HELP)

    def parse_result(self, result) -> str:
        pass

    def execute(self, args: list[str]) -> None:
        try:
            self.parse(args)
            for _ in range(0, SCRIPT_3_ROTATE_CNT):
                value = f'0x{random.getrandbits(32):08X}'

                self.write_cmd.execute(f'0 {value}'.split())
                self.write_cmd.execute(f'99 {value}'.split())

                val_lba_0 = self.read_cmd.execute(['0'])
                val_lba_99 = self.read_cmd.execute(['99'])

                if val_lba_0 != value or val_lba_99 != value:
                    print('[3_WriteReadAging] FAIL')
                    return

            print('[3_WriteReadAging] PASS')
        except ValueError:
            self._logger.error(Msg.ERROR)
