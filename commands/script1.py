import random

from commands.mixin import WriteSupportMixin, ReadSupportMixin, RandomValueGenerateMixin
from commands.base import Command
from shell_tool.shell_constants import MAX_LBA, SCRIPT_1_STEP, ShellMsg, ShellPrefix
from shell_tool.shell_logger import Logger


class FullWriteAndReadCompare(
    WriteSupportMixin,
    ReadSupportMixin,
    RandomValueGenerateMixin,
    Command,
):
    expected_num_args = 0
    help_msg = ShellMsg.SCRIPT_1_HELP

    def __init__(self, logger: Logger, prefix=ShellPrefix.SCRIPT_1):
        super().__init__(logger, prefix)
        self.max_lba = MAX_LBA
        self.step = SCRIPT_1_STEP

    def execute(self, args=None):
        try:
            self._parse(args)
            random_values = self.randvals(self.max_lba, self.step, unique=True)
            self._logger.print_and_log(prefix=self._prefix)
            for chunk_index, current_value in enumerate(random_values):
                current_start = chunk_index * self.step
                current_end = min(current_start + self.step - 1, self.max_lba) + 1

                # Execute Write
                for lba in range(current_start, current_end):
                    self.write(lba, current_value)

                # Read and Verify
                for lba in range(current_start, current_end):
                    if not self.read_with_verify(lba, current_value):
                        self._logger.print_and_log(self._prefix, ShellMsg.FAIL)
                        return True
            self._logger.print_and_log(self._prefix, ShellMsg.PASS)
        except ValueError:
            self._logger.print_and_log(self._prefix, ShellMsg.ERROR)
        return True
