import random

from commands.base import Command
from commands.read import ReadCommand
from commands.write import WriteCommand
from shell_constants import SCRIPT_3_ROTATE_CNT, ShellMsg, ShellPrefix
from shell_logger import Logger


class WriteReadAging(Command):
    def __init__(self, logger: Logger, prefix=ShellPrefix.SCRIPT_3):
        super().__init__(logger, prefix)
        self._write_cmd = WriteCommand(self._logger, prefix=None)
        self._read_cmd = ReadCommand(self._logger, prefix=None)

    def parse(self, args: list[str]) -> list[str]:
        pass

    def parse_result(self, result) -> str:
        pass

    def execute(self, args=None) -> bool:
        self._logger.print_blank_line()
        self._logger.print_and_log(self._prefix, None)
        for _ in range(0, SCRIPT_3_ROTATE_CNT):
            value = f'0x{random.getrandbits(32):08X}'

            self._write_cmd.execute(f'0 {value}'.split())
            self._write_cmd.execute(f'99 {value}'.split())
            self._read_cmd.execute(['0'])
            val_lba_0 = self._read_cmd.result
            self._read_cmd.execute(['99'])
            val_lba_99 = self._read_cmd.result

            if val_lba_0 != value or val_lba_99 != value:
                self._logger.print_and_log(self._prefix, ShellMsg.FAIL)
                return True
        self._logger.print_and_log(self._prefix, ShellMsg.PASS)
        return True
