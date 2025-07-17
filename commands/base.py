from abc import abstractmethod
import subprocess
from subprocess import CalledProcessError

from commands.command_interface import CommandInterface
from commands.validator import Validator
from shell_tool.shell_constants import (
    LBA_RANGE,
    RUN_SSD,
    SIZE_RANGE,
    SSD_OUTPUT_FILE,
    Hex,
    ShellMsg,
)
from shell_tool.shell_logger import Logger


class Command(CommandInterface):
    expected_num_args: int | None = None
    help_msg: str = ShellMsg.HELP
    command = ''

    def __init__(self, logger: Logger, prefix=None):
        self._logger = logger
        self._result = None
        self._prefix = prefix
        self._validators: list[Validator] = []

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        self._result = result

    def _parse(self, args: list[str]) -> list[str]:
        args = args or []
        self._check_argument_count(args)
        try:
            for validator in self._validators:
                validator.validate(args)
        except ValueError as e:
            self._logger.print(prefix='[ERROR]', message=str(e))
            raise
        return [self.command] + args

    @abstractmethod
    def _parse_result(self, result: str) -> str:
        raise NotImplementedError

    def _check_argument_count(self, args: list[str]):
        if self.expected_num_args is not None:
            if len(args) != self.expected_num_args:
                self._logger.log(
                    f'Invalid argument count: '
                    f'expected {self.expected_num_args}, got {len(args)}'
                )
                raise ValueError(self.help_msg)

    def _check_lba(self, lba: str) -> bool:
        if lba.isdigit() and int(lba) in LBA_RANGE:
            return True
        self._logger.log(f'Invalid LBA: {lba}')
        raise ValueError

    def _check_data(self, data: str) -> bool:
        if (
            data.startswith(Hex.PREFIX)
            and len(data) == Hex.LENGTH
            and all(c in Hex.RANGE for c in data[2:])
        ):
            return True
        self._logger.log(f'Invalid hex data: {data}')
        raise ValueError

    def _check_size(self, size: str) -> bool:
        if size.isdigit() and int(size) in SIZE_RANGE:
            return True
        raise ValueError(f'Invalid size: {size}')

    def _check_boundary(self, lba: str, size: str) -> bool:
        if int(lba) + int(size) - 1 <= max(LBA_RANGE):
            return True
        raise ValueError('Erase range exceeds device limit.')

    def _run_sdd(self, args):
        cmd = RUN_SSD + args
        self._logger.log('Executing command:' + ' '.join(cmd))
        subprocess.run(cmd, check=True)

    def _process_result(self):
        """Reads result file and logs parsed result."""
        with open(SSD_OUTPUT_FILE) as f:
            self.result = f.read().strip()
            parsed_result = self._parse_result(self.result)
            self._logger.print_and_log(self._prefix, parsed_result)

    def execute(self, args: list[str] = None) -> bool:
        try:
            parsed_args = self._parse(args)
            self._run_sdd(parsed_args)
            self._process_result()
        except ValueError:
            self._logger.print(message=self.help_msg)
        except CalledProcessError:
            self._logger.print_and_log(self._prefix, ShellMsg.ERROR)
        return True
