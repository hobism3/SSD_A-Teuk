from commands.base import Command
from logger import Logger
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class ReadCommand(Command):
    def __init__(self, ssd):
        self._ssd = ssd
        self._logger = Logger(Pre.READ)

    def execute(self, args) -> bool:
        if len(args) != 1:
            self._logger.error(Msg.READ_HELP)
            return True

        try:
            lba = int(args[0])
            self._logger.info(f'LBA: {lba}')
            self._ssd.read(lba)
            self._logger.info(Msg.DONE)
        except ValueError:
            self._logger.error(Msg.ERROR)
        return True
