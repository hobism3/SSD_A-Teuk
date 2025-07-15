from commands.base import ExitCommand, HelpCommand
from commands.read import ReadCommand
from commands.script1 import FullWriteAndReadCompare
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
            Cmd.SCRIPT_1_FULL: FullWriteAndReadCompare(),
            Cmd.SCRIPT_1_SHORT: FullWriteAndReadCompare(),
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
        if not cmd:
            return True
        parts = cmd.split()
        command_name = parts[0].lower()
        command = self._command_map.get(command_name)
        if command:
            return command.execute(parts[1:])
        else:
            print(Msg.INVALID)
            return True


if __name__ == '__main__':
    Shell().run()
