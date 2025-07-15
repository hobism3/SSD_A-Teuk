from commands.base import ExitCommand, HelpCommand
from commands.full_read import FullReadCommand
from commands.full_write import FullWriteCommand
from commands.read import ReadCommand
from commands.script2 import PartialLBAWriteCommand
from commands.write import WriteCommand
from shell_constants import ShellCmd as Cmd
from shell_constants import ShellMsg as Msg


class Shell:
    def __init__(self, ssd):
        self._ssd = ssd
        self._command_map = {
            Cmd.WRITE: WriteCommand(),
            Cmd.READ: ReadCommand(),
            Cmd.EXIT: ExitCommand(),
            Cmd.HELP: HelpCommand(),
            Cmd.FULLREAD: FullReadCommand(),
            Cmd.FULLWRITE: FullWriteCommand(),
            Cmd.PARTIALLBAWRITE_SHORT: PartialLBAWriteCommand(),
            Cmd.PARTIALLBAWRITE_LONG: PartialLBAWriteCommand(),
        }

    def run(self):
        flag = True
        while flag:
            try:
                flag = self.command(input(Msg.PROMPT).strip())
            except (EOFError, KeyboardInterrupt):
                break

    def command(self, cmd: str) -> bool:
        if not cmd:
            return True
        parts = cmd.split()
        command_name = parts[0].lower()
        command = self._command_map.get(command_name)
        if command:
            return command.execute(parts[1:], self._ssd)
        else:
            print(Msg.INVALID)
            return True
