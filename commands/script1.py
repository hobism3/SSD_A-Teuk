import random

from commands.base import Command
from commands.read import ReadCommand
from commands.write import WriteCommand
from logger import Logger
from shell_constants import MAX_LBA, SCRIPT_1_STEP
from shell_constants import ShellPrefix as Pre


class FullWriteAndReadCompare(Command):
    def __init__(self):
        self._logger = Logger(Pre.SCRIPT_1)
        self.max_lba = MAX_LBA
        self.step = SCRIPT_1_STEP
        self.write_cmd = WriteCommand()
        self.read_cmd = ReadCommand()

    def parse(self, args: list[str]) -> list[str]:
        pass

    def parse_result(self, result) -> str:
        pass

    def execute(self, args):
        used_values = set()
        current_start = 0

        while current_start <= self.max_lba:
            current_end = min(current_start + self.step - 1, self.max_lba)

            # 중복 없는 랜덤값 생성
            while True:
                current_value = f'0x{random.getrandbits(32):08X}'
                if current_value not in used_values:
                    used_values.add(current_value)
                    break

            # Write 명령어 수행
            for lba in range(current_start, current_end + 1):
                cmd = f'{lba} {current_value}'
                parts = cmd.split()
                self.write_cmd.execute(parts)

            # Read 후 값 확인
            for lba in range(current_start, current_end + 1):
                read_value = self.read_cmd.execute(f'{lba}')

                if read_value != current_value:
                    print('[1_FullWriteAndReadCompare] FAIL')
                    return

            current_start = current_end + 1

        print('[1_FullWriteAndReadCompare] PASS')
