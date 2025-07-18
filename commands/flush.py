from commands.base import Command, command_handler
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class FlushCommand(Command):
    expected_num_args = 0
    help_msg = Msg.FLUSH_HELP
    command = 'F'

    def __init__(self, logger: Logger, prefix=Pre.FLUSH):
        super().__init__(logger, prefix)

    def _parse(self, args: list[str]) -> list[str]:
        args = args or []
        self._check_argument_count(args)
        return [self.command]

    def _parse_result(self, result: int) -> str:
        return Msg.DONE if not result.strip() else Msg.ERROR

    @command_handler
    def execute(self, args: list[str]) -> bool:
        parsed_args = self._parse(args)
        self._run_ssd(parsed_args)
        self._process_result()
        return True
