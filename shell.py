import sys
import threading
import time

from shell_tool.shell_command_factory import ShellCommandFactory
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_logger import Logger


class Shell:
    def __init__(self):
        self.logger = Logger()
        self._prefix = 'SHELL'
        self._factory = ShellCommandFactory(self.logger)

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
        self.logger.verbose = False
        logger = Logger(verbose=True)
        try:
            with open(path) as f:
                scripts = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.print(prefix, f'Script file not found - {path}')
            return
        for script in scripts:
            script_name = script.split()[0]
            if not self._factory.is_script(script_name):
                logger.log(f'{script_name} is not valid script')
                continue
            logger.print(message=f'{script:<30} ___   Run', end='', flush=True)
            success = self._run_with_dots(script, logger)
            logger.print(message='Pass' if success else 'FAIL!')

    def _run_with_dots(self, script: str, logger) -> bool:
        done_flag = {'done': False}
        result_flag = {'success': True}

        def _dot_task():
            while not done_flag['done']:
                logger.dot()
                time.sleep(1)

        thread = threading.Thread(target=_dot_task)
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
        command_instance = self._factory.get(command_name)
        return command_instance.execute(parts[1:])


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) == 2 else None
    Shell().run(path)
