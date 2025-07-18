from abc import abstractmethod
from functools import wraps
import os
import subprocess
from subprocess import CalledProcessError

from commands.command_interface import CommandInterface
from commands.validator import *
from shell_tool.shell_constants import (
    RUN_SSD,
    SSD_OUTPUT_FILE,
    ShellMsg,
)
from shell_tool.shell_logger import Logger


def command_handler(func):
    error_prefix = '[ERROR]'

    @wraps(func)
    def wrapper(self, args=None):
        try:
            return func(self, args)
        except ValueError as e:
            self._logger.print_and_log(error_prefix, str(e))
            self._logger.print(message=self.help_msg)
        except CalledProcessError:
            self._logger.print_and_log(self._prefix, ShellMsg.ERROR)
        return True

    return wrapper


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
        for validator in self._validators:
            validator.validate(args)
        return [self.command] + args

    def _check_argument_count(self, args: list[str]):
        if self.expected_num_args is not None:
            if len(args) != self.expected_num_args:
                raise ValueError(
                    f'Invalid argument count: expected {self.expected_num_args}, got {len(args)}'
                )

    @abstractmethod
    def _parse_result(self, result: str) -> str:
        raise NotImplementedError

    def _run_ssd(self, args):
        cmd = RUN_SSD + args
        short_cmd = [os.path.basename(part) for part in cmd]
        self._logger.log('Executing command:' + ' '.join(short_cmd))
        subprocess.run(cmd, check=True)

    def _process_result(self):
        """Reads result file and logs parsed result."""
        with open(SSD_OUTPUT_FILE) as f:
            self.result = f.read().strip()
            parsed_result = self._parse_result(self.result)
            self._logger.print_and_log(self._prefix, parsed_result)

    @command_handler
    def execute(self, args: list[str] = None) -> bool:
        parsed_args = self._parse(args)
        self._run_ssd(parsed_args)
        self._process_result()
        return True
