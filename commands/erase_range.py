from commands.base import Command
from commands.erase import EraseCommand
from shell_constants import LBA_RANGE
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre
from shell_logger import Logger


class EraseRangeCommand(Command):
    def __init__(self):
        self._logger = Logger(Pre.ERASERANGE)
        self._erase_cmd = EraseCommand()

    def execute(self, args: list[str]) -> bool:
        try:
            start_lba, size = self._parse_erase_range_args(args)
            self._execute_erase(start_lba, size)
            self._logger.info(Msg.DONE)
        except ValueError:
            self._logger.error(Msg.ERROR)
        return True

    def parse(self, args: list[str]) -> list[str]:
        if len(args) != 2:
            raise ValueError(Msg.ERASE_RANGE_HELP)
        start_lba, end_lba = args
        self._check_validity(start_lba, end_lba)

        return [start_lba, end_lba]

    def parse_result(self, result) -> str:
        pass

    def _execute_erase(self, lba: int, size: int) -> None:
        cmd = f'{lba} {size}'
        self._erase_cmd.execute(cmd.split())

    def _parse_erase_range_args(self, args: list[str]) -> tuple[int, int]:
        ssd_args = self.parse(args)
        start_lba = int(ssd_args[0])
        end_lba = int(ssd_args[1])
        size = end_lba - start_lba + 1
        return start_lba, size

    def _check_validity(self, start_lba: str, end_lba: str) -> None:
        if not (self._check_lba(start_lba) and self._check_lba(end_lba)):
            raise ValueError(
                f'LBA must be an integer between {LBA_RANGE[0]} and {LBA_RANGE[-1]}'
            )
        if start_lba > end_lba:
            raise ValueError('Start LBA must be less than End LBA')
