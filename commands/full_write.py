import subprocess

from commands.base import Command
from logger import Logger
from shell_constants import LBA_RANGE, RUN_SSD, SSD_OUTPUT_FILE
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class FullWriteCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.READ)
        self._lba = None

    def parse(self, args: list[str]) -> list[str]:
        if len(args) != 1:
            raise ValueError(Msg.WRITE_HELP)
        data = args[0]
        if not self._check_data(data):
            raise ValueError('Data must be a hex string like 0x0129ABCF')
        return ['W', self._lba, data]

    def execute(self, args) -> bool:
        try:
            for index in LBA_RANGE:
                self._lba = f'{index}'
                ssd_args = self.parse(args)
                return_code = subprocess.run(RUN_SSD + ssd_args, check=True)
                if return_code.returncode != 0:
                    self._logger.error(Msg.ERROR)
                with open(SSD_OUTPUT_FILE) as f:
                    result = self.parse_result(f.read().strip())
                self._logger.info(result)
        except ValueError:
            self._logger.error(Msg.ERROR)
        return True

    def parse_result(self, result) -> str:
        if not result:
            return Pre.FULLWRITE + Msg.DONE
        return Msg.ERROR
