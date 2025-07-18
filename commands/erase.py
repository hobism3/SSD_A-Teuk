from commands.base import Command, command_handler
from commands.validator import Validator
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class EraseCommand(Command):
    expected_num_args = 2
    help_msg = Msg.ERASE_HELP
    command = 'E'

    def __init__(self, logger: Logger, prefix=Pre.ERASE):
        super().__init__(logger, prefix)
        self._chunk_size = 10
        self._validators: list[Validator] = [
            Validator(self._check_lba, (0,)),
            Validator(self._check_size, (1,)),
            Validator(self._check_boundary, (0, 1)),
        ]

    def _parse(self, args):
        parsed_args = super()._parse(args)
        self._lba = int(args[0])
        self._size = int(args[1])
        return parsed_args

    def _parse_result(self, result: str) -> str:
        return Msg.DONE if not result.strip() else Msg.ERROR

    @command_handler
    def execute(self, args: list[str] = None) -> bool:
        self._parse(args)
        self._execute_chunks(self._lba, self._size, self._chunk_size)
        self._process_result()
        return True

    def _execute_chunks(self, start: int, size: int, chunk_size: int = 10):
        end = start + size
        for lba in range(start, end, chunk_size):
            size = min(chunk_size, end - lba)
            self._run_sdd([self.command, str(lba), str(size)])
