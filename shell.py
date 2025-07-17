from commands.base import ExitCommand, HelpCommand
from commands.erase import EraseCommand
from commands.erase_range import EraseRangeCommand
from commands.full_read import FullReadCommand
from commands.full_write import FullWriteCommand
from commands.read import ReadCommand
from commands.script1 import FullWriteAndReadCompare
from commands.script2 import PartialLBAWriteCommand
from commands.script3 import WriteReadAging
from commands.write import WriteCommand
from shell_constants import ShellCmd as Cmd
from shell_constants import ShellMsg as Msg


class Shell:
    def __init__(self):
        self._command_map = {
            Cmd.WRITE: WriteCommand(),
            Cmd.READ: ReadCommand(),
            Cmd.EXIT: ExitCommand(),
            Cmd.HELP: HelpCommand(),
            Cmd.FULLREAD: FullReadCommand(),
            Cmd.FULLWRITE: FullWriteCommand(),
            Cmd.SCRIPT_1_FULL: FullWriteAndReadCompare(),
            Cmd.SCRIPT_1_SHORT: FullWriteAndReadCompare(),
            Cmd.SCRIPT_2_FULL: PartialLBAWriteCommand(),
            Cmd.SCRIPT_2_SHORT: PartialLBAWriteCommand(),
            Cmd.SCRIPT_3_FULL: WriteReadAging(),
            Cmd.SCRIPT_3_SHORT: WriteReadAging(),
            Cmd.ERASE: EraseCommand(),
            Cmd.ERASERANGE: EraseRangeCommand(),
        }

    def run(self):
        flag = True
        while flag:
            try:
                flag = self.command(input(Msg.PROMPT).strip())
            except (EOFError, KeyboardInterrupt):
                return False
        return True

    def command(self, cmd: str) -> bool:
        if not cmd.strip():
            return True
        parts = cmd.split()
        command_name = parts[0]
        command = self._command_map.get(command_name)
        if command:
            return command.execute(parts[1:])
        else:
            print(Msg.INVALID)
            return True


if __name__ == '__main__':
    Shell().run()
