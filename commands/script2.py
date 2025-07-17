import random

from commands.script import ScriptCommand
from shell_constants import ShellMsg
from shell_constants import ShellPrefix as Pre
from shell_logger import Logger


class PartialLBAWriteCommand(ScriptCommand):
    def __init__(self, logger: Logger, prefix=Pre.SCRIPT_2):
        super().__init__(logger, prefix)
        self._lba = None
        self._random_value = random.randint(0x00000000, 0xFFFFFFFF)

    def execute(self, args=None) -> bool:
        try:
            sample_index = ['4', '0', '3', '1', '2']
            self._logger.print_blank_line()
            self._logger.print_and_log(self._prefix)
            for _ in range(30):
                hex_string = f'0x{self._random_value:08X}'
                for index in sample_index:
                    self.write(index, hex_string)

                for index in sample_index:
                    success = self.read_with_verify(index, hex_string)
                    if not success:
                        self._logger.print_and_log(self._prefix, ShellMsg.FAIL)
                        return True
                self._logger.print_and_log(self._prefix, ShellMsg.PASS)
        except ValueError:
            self._logger.print_and_log(self._prefix, ShellMsg.ERROR)
        return True
