import sys
import threading
import time

from commands.base import ExitCommand, HelpCommand
from commands.full_read import FullReadCommand
from commands.full_write import FullWriteCommand
from commands.read import ReadCommand
from commands.script1 import FullWriteAndReadCompare
from commands.script2 import PartialLBAWriteCommand
from commands.script3 import WriteReadAging
from commands.write import WriteCommand
from shell_constants import ShellCmd as Cmd
from shell_constants import ShellMsg as Msg
from shell_logger import Logger


class Shell:
    def __init__(self):
        self.logger = Logger()
        self._prefix = 'SHELL'
        self._command_map = {
            Cmd.WRITE: WriteCommand,
            Cmd.READ: ReadCommand,
            Cmd.EXIT: ExitCommand,
            Cmd.HELP: HelpCommand,
        }
        self._script_map = {
            Cmd.FULLREAD: FullReadCommand,
            Cmd.FULLWRITE: FullWriteCommand,
            Cmd.SCRIPT_1_FULL: FullWriteAndReadCompare,
            Cmd.SCRIPT_1_SHORT: FullWriteAndReadCompare,
            Cmd.SCRIPT_2_FULL: PartialLBAWriteCommand,
            Cmd.SCRIPT_2_SHORT: PartialLBAWriteCommand,
            Cmd.SCRIPT_3_FULL: WriteReadAging,
            Cmd.SCRIPT_3_SHORT: WriteReadAging,
        }

    def run(self, serial_path: str = None):
        if serial_path:
            self.run_serial_script(serial_path)
        else:
            self.run_interactive()

    def run_interactive(self):
        flag = True
        while flag:
            try:
                flag = self.command(input(Msg.PROMPT).strip())
            except (EOFError, KeyboardInterrupt):
                break

    def run_serial_script(self, path: str):
        prefix = '[Runner]'
        self.logger.set_verbose(False)
        logger = Logger(verbose=True)
        try:
            with open(path) as f:
                scripts = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.print(prefix, f'Script file not found - {path}')
            return
        for script in scripts:
            script_name = script.split()[0]
            if script_name not in self._script_map:
                logger.log(f'{script_name} is not valid script')
                continue
            logger.print(None, f'{script:<30} ___   Run', end='', flush=True)
            success = self._run_with_dots(script, logger)
            logger.print(None, 'Pass' if success else 'FAIL!')

    def _run_with_dots(self, script: str, logger) -> bool:
        done_flag = {'done': False}
        result_flag = {'success': True}

        def _dot_task():
            while not done_flag['done']:
                logger.dot()
                time.sleep(1)

        thread = threading.Thread(target=_dot_task, args=(done_flag,))
        thread.start()
        try:
            result_flag['success'] = self.command(script)
        finally:
            done_flag['done'] = True
            thread.join()

        return result_flag['success']

    def command(self, cmd: str) -> bool:
        if not cmd.strip():
            return True
        parts = cmd.split()
        command_name = parts[0]
        command_cls = self._script_map.get(command_name) or self._command_map.get(
            command_name, HelpCommand
        )
        return command_cls(self.logger).execute(parts[1:])


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) == 2 else None
    Shell().run(path)
