import random

from commands.script import ScriptCommand
from shell_constants import MAX_LBA, SCRIPT_1_STEP, ShellMsg, ShellPrefix
from shell_logger import Logger


class FullWriteAndReadCompare(ScriptCommand):
    def __init__(self, logger: Logger, prefix=ShellPrefix.SCRIPT_1):
        super().__init__(logger, prefix)
        self.max_lba = MAX_LBA
        self.step = SCRIPT_1_STEP

    def execute(self, args=None):
        random_values = self._generate_random_value_lst()
        self._logger.print_blank_line()
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
        return True

    def _generate_random_value_lst(self):
        num_chunks = (self.max_lba + self.step) // self.step
        random_values = [
            f'0x{val:08X}' for val in random.sample(range(0x100000000), num_chunks)
        ]
        return random_values
