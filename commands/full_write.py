from commands.script import ScriptCommand
from shell_tool.shell_constants import LBA_RANGE
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger


class FullWriteCommand(ScriptCommand):
    def __init__(self, logger: Logger, prefix=Pre.FULLWRITE):
        super().__init__(logger, prefix)
        self._lba = None

    def execute(self, args=None) -> bool:
        try:
            for index in LBA_RANGE:
                self.write(index, args[0])
                self._logger.print_and_log(self._prefix, Msg.DONE)
        except ValueError:
            self._logger.print_and_log(self._prefix, Msg.ERROR)
        return True
