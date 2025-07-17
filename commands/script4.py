import random

from commands.erase import EraseCommand
from commands.script import ScriptCommand
from commands.write import WriteCommand
from shell_logger import Logger
from shell_constants import MAX_LBA
from shell_constants import Script as Const
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class EraseAndWriteAging(ScriptCommand):
    def __init__(self, logger: Logger, prefix: object = Pre.SCRIPT_4) -> None:
        super().__init__(logger, prefix)
        self._lba = 0
        self._erase = EraseCommand(self._logger, prefix=None)

    def execute(self, args: list[str]) -> bool:
        try:
            self._execute_erase()
            for _ in range(30):
                for __ in range(49):
                    self._write_multiple(times=2, value=self.get_random_hex_string())
                    self._execute_erase()
                self._logger.print_and_log(self._prefix, Msg.PASS)
        except ValueError:
            self._logger.print_and_log(self._prefix, Msg.ERROR)
        return True

    def _write_multiple(self, times=2, value=''):
        for _ in range(times):
            self.write(self._lba, value)

    def _execute_erase(self):
        ssd_args = self.get_lba_and_size_to_erase()
        self._erase.execute(ssd_args)
        self._lba += Const.STEP_LBA

    def get_random_hex_string(self):
        return f'0x{random.randint(0x00000000, 0xFFFFFFFF):08X}'

    def get_lba_and_size_to_erase(self) -> list[str]:
        size_erase = min(Const.DEFAULT_ERASE_SIZE, MAX_LBA - self._lba + 1)
        return [str(self._lba), str(size_erase)]
