from subprocess import CalledProcessError

from commands.base import Command
from commands.mixin import RandomValueGenerateMixin, ReadSupportMixin, WriteSupportMixin
from shell_tool.shell_constants import SCRIPT_3_ROTATE_CNT, ShellMsg, ShellPrefix
from shell_tool.shell_logger import Logger


class WriteReadAging(
    WriteSupportMixin, RandomValueGenerateMixin, ReadSupportMixin, Command
):
    expected_num_args = 0
    help_msg = ShellMsg.SCRIPT_3_HELP

    def __init__(self, logger: Logger, prefix=ShellPrefix.SCRIPT_3):
        super().__init__(logger, prefix)

    def execute(self, args=None) -> bool:
        try:
            self._parse(args)
            self._logger.print_and_log(self._prefix)
            for _ in range(0, SCRIPT_3_ROTATE_CNT):
                value = self.rand32()
                self.write(0, value)
                self.write(99, value)
                success_0 = self.read_with_verify(0, value)
                success_99 = self.read_with_verify(99, value)
                if not success_0 or not success_99:
                    self._logger.print_and_log(self._prefix, ShellMsg.FAIL)
                    return True
            self._logger.print_and_log(self._prefix, ShellMsg.PASS)
        except ValueError:
            self._logger.print(message=self.help_msg)
        except CalledProcessError:
            self._logger.print_and_log(self._prefix, ShellMsg.ERROR)
        return True
