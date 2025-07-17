import random

from commands.base import Command
from commands.read import ReadCommand
from commands.write import WriteCommand
from logger import Logger
from shell_constants import MAX_LBA, SCRIPT_1_STEP
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class FullWriteAndReadCompare(Command):
    def __init__(self):
        self._logger = Logger(Pre.SCRIPT_1)
        self.max_lba = MAX_LBA
        self.step = SCRIPT_1_STEP
        self.write_cmd = WriteCommand()
        self.read_cmd = ReadCommand()

    def parse(self, args: list[str]) -> None:
        if len(args) != 0:
            raise ValueError(Msg.SCRIPT_1_HELP)

    def parse_result(self, result) -> str:
        pass

    def execute(self, args: list[str]) -> None:
        try:
            self.parse(args)
            random_values = self._generate_random_value_lst()
            current_start = 0
            chunk_index = 0

            while current_start <= self.max_lba:
                current_end = min(current_start + self.step - 1, self.max_lba)
                current_value = random_values[chunk_index]

                # Execute Write
                for lba in range(current_start, current_end + 1):
                    self._execute_write(lba, current_value)

                # Read and Verify
                for lba in range(current_start, current_end + 1):
                    if not self._execute_read_verify(lba, current_value):
                        return

                current_start = current_end + 1
                chunk_index += 1

            print('[1_FullWriteAndReadCompare] PASS')
        except ValueError:
            self._logger.error(Msg.ERROR)

    def _generate_random_value_lst(self):
        num_chunks = (self.max_lba + self.step) // self.step
        random_values = [
            f'0x{val:08X}' for val in random.sample(range(0x100000000), num_chunks)
        ]
        return random_values

    def _execute_write(self, lba, current_value):
        cmd = f'{lba} {current_value}'
        self.write_cmd.execute(cmd.split())

    def _execute_read_verify(self, lba, current_value):
        read_value = self.read_cmd.execute([f'{lba}'])
        if read_value != current_value:
            print('[1_FullWriteAndReadCompare] FAIL')
            return False
        return True
