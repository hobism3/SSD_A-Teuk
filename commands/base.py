from logger import Logger
from shell_constants import ShellMsg as Msg


class Command:
    def execute(self, args):
        raise NotImplementedError


class ExitCommand(Command):
    def execute(self, args) -> bool:
        return False


class HelpCommand(Command):
    def __init__(self):
        self._logger = Logger()

    def execute(self, args) -> bool:
        self._logger.info(Msg.HELP)
        return True
