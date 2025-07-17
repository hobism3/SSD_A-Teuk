import random

from commands.base import Command
from commands.erase import EraseCommand
from commands.write import WriteCommand
from commands.mixin import WriteSupportMixin, RandomValueGenerateMixin, EraseSupportMixin, WritePatternMixin
from shell_tool.shell_constants import MAX_LBA
from shell_tool.shell_constants import Script4 as Const
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class EraseAndWriteAging(
    WriteSupportMixin, 
    WritePatternMixin,
    EraseSupportMixin,
    RandomValueGenerateMixin,
    Command
):
    expected_num_args = 0
    help_msg = Msg.SCRIPT_4_HELP

    def __init__(self, logger: Logger, prefix=Pre.SCRIPT_4):
        super().__init__(logger, prefix)
        self._lba = 0
    
    def execute(self, args: list[str] = None) -> bool:
        try:
            self._parse(args)
            self._erase_once_move_lba()
            for _ in range(Const.LOOP1):
                for _ in range(Const.LOOP2):
                    self.write_random_n(self._lba, 2)
                    self._erase_once_move_lba()
            self._logger.print_and_log(self._prefix, Msg.PASS)
        except ValueError:
            self._logger.print_and_log(self._prefix, Msg.ERROR)
        return True

    def _erase_once_move_lba(self):
        size = min(Const.DEFAULT_ERASE_SIZE, MAX_LBA - self._lba + 1)
        self.erase(self._lba, size)
        next_lba = self._lba + Const.STEP_LBA
        self._lba = Const.STEP_LBA if next_lba > MAX_LBA else next_lba
