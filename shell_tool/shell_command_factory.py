from commands.meta import ExitCommand, HelpCommand
from commands.erase import EraseCommand
from commands.erase_range import EraseRangeCommand
from commands.flush import FlushCommand
from commands.full_read import FullReadCommand
from commands.full_write import FullWriteCommand
from commands.read import ReadCommand
from commands.script1 import FullWriteAndReadCompare
from commands.script2 import PartialLBAWriteCommand
from commands.script3 import WriteReadAging
from commands.script4 import EraseAndWriteAging
from commands.write import WriteCommand
from shell_tool.shell_constants import ShellCmd as Cmd
from shell_tool.shell_logger import Logger


class ShellCommandFactory:
    def __init__(self, logger: Logger):
        self.logger = logger
        self._command_creators = {
            Cmd.WRITE: lambda: WriteCommand(self.logger),
            Cmd.READ: lambda: ReadCommand(self.logger),
            Cmd.EXIT: lambda: ExitCommand(self.logger),
            Cmd.HELP: lambda: HelpCommand(self.logger),
            Cmd.FLUSH: lambda: FlushCommand(self.logger),
            Cmd.ERASE: lambda: EraseCommand(self.logger),
        }
        self._script_creators = {
            Cmd.FULLREAD: lambda: FullReadCommand(self.logger),
            Cmd.FULLWRITE: lambda: FullWriteCommand(self.logger),
            Cmd.SCRIPT_1_FULL: lambda: FullWriteAndReadCompare(self.logger),
            Cmd.SCRIPT_1_SHORT: lambda: FullWriteAndReadCompare(self.logger),
            Cmd.SCRIPT_2_FULL: lambda: PartialLBAWriteCommand(self.logger),
            Cmd.SCRIPT_2_SHORT: lambda: PartialLBAWriteCommand(self.logger),
            Cmd.SCRIPT_3_FULL: lambda: WriteReadAging(self.logger),
            Cmd.SCRIPT_3_SHORT: lambda: WriteReadAging(self.logger),
            Cmd.ERASERANGE: lambda: EraseRangeCommand(self.logger),
            Cmd.SCRIPT_4_FULL: lambda: EraseAndWriteAging(self.logger),
            Cmd.SCRIPT_4_SHORT: lambda: EraseAndWriteAging(self.logger),
        }

    def is_command(self, cmd_name: str):
        return cmd_name in self._command_creators

    def is_script(self, cmd_name: str):
        return cmd_name in self._script_creators

    def get(self, cmd_name: str):
        if self.is_command(cmd_name):
            return self._command_creators[cmd_name]()
        if self.is_script(cmd_name):
            return self._script_creators[cmd_name]()
        return HelpCommand(self.logger)
