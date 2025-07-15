from commands.base import ExitCommand, HelpCommand
from commands.read import ReadCommand
from commands.write import WriteCommand
from shell_constants import ShellCmd as Cmd
from shell_constants import ShellMsg as Msg


class Shell:
    def __init__(self, ssd):
        self._ssd = ssd
        self._command_map = {
            Cmd.WRITE: WriteCommand(ssd),
            Cmd.READ: ReadCommand(ssd),
            Cmd.EXIT: ExitCommand(),
            Cmd.HELP: HelpCommand(),
        }

    def run(self):
        flag = True
        while flag:
            try:
                cmd = input(Msg.PROMPT).strip()
                flag = self.command(cmd)
            except (EOFError, KeyboardInterrupt):
                break

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
