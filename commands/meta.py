from commands.command_interface import CommandInterface
from shell_tool.shell_constants import ShellMsg
from shell_tool.shell_logger import Logger


class MetaCommand(CommandInterface):
    def __init__(self, logger: Logger):
        self._logger = logger


class ExitCommand(MetaCommand):
    def execute(self, args: list[str] = None) -> bool:
        self._logger.print(message='bye bye')
        self._logger.log('User exited the shell.')
        return False


class HelpCommand(MetaCommand):
    def execute(self, args: list[str] = None) -> bool:
        self._logger.print(message=ShellMsg.HELP)
        return True
