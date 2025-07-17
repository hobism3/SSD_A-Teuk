import random

from commands.script import ScriptCommand
from shell_constants import SCRIPT_3_ROTATE_CNT, ShellMsg, ShellPrefix
from shell_logger import Logger


class WriteReadAging(ScriptCommand):
    def __init__(self, logger: Logger, prefix=ShellPrefix.SCRIPT_3):
        super().__init__(logger, prefix)

    def execute(self, args=None) -> bool:
        self._logger.print_blank_line()
        self._logger.print_and_log(self._prefix)
        for _ in range(0, SCRIPT_3_ROTATE_CNT):
            value = f'0x{random.getrandbits(32):08X}'
            self.write(0, value)
            self.write(99, value)
            success_0 = self.read_with_verify(0, value)
            success_99 = self.read_with_verify(99, value)
            if not success_0 or not success_99:
                self._logger.print_and_log(self._prefix, ShellMsg.FAIL)
                return True
        self._logger.print_and_log(self._prefix, ShellMsg.PASS)
        return True
