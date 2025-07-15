from commands.base import Command
from logger import Logger
from shell_constants import LBA_RANGE, Hex
from shell_constants import ShellMsg as Msg
from shell_constants import ShellPrefix as Pre


class WriteCommand(Command):
    def __init__(self, ssd):
        self._ssd = ssd
        self._logger = Logger(Pre.WRITE)

    def execute(self, args):
        if len(args) != 2:
            self._logger.error(Msg.ERROR)
            return True

        try:
            lba = int(args[0])
            data = args[1]

            if lba not in LBA_RANGE:
                self._logger.error(Msg.ERROR)
                return True

            if not (
                data.startswith(Hex.PREFIX)
                and len(data) == Hex.LENGTH
                and all(c in Hex.RANGE for c in data[2:])
            ):
                self._logger.error(Msg.ERROR)
                return True

            self._ssd.execute(lba, data)
            self._logger.info(Msg.DONE)
        except ValueError:
            self._logger.error(Msg.ERROR)
        return True
