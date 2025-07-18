from subprocess import CalledProcessError

from commands.base import Command
from commands.mixin import RandomValueGenerateMixin, ReadSupportMixin, WriteSupportMixin
from shell_tool.shell_constants import ShellMsg, ShellPrefix
from shell_tool.shell_logger import Logger


class PartialLBAWriteCommand(
    WriteSupportMixin, RandomValueGenerateMixin, ReadSupportMixin, Command
):
    expected_num_args = 0
    help_msg = ShellMsg.SCRIPT_2_HELP

    def __init__(self, logger: Logger, prefix=ShellPrefix.SCRIPT_2):
        super().__init__(logger, prefix)

    def execute(self, args=None) -> bool:
        sample_index = ['4', '0', '3', '1', '2']
        try:
            self._parse(args)
            self._logger.print_and_log(self._prefix)
            for _ in range(30):
                hex_string = self.rand32()
                for index in sample_index:
                    self.write(index, hex_string)

                for index in sample_index:
                    success = self.read_with_verify(index, hex_string)
                    if not success:
                        self._logger.print_and_log(self._prefix, ShellMsg.FAIL)
                        return True
            self._logger.print_and_log(self._prefix, ShellMsg.PASS)
        except ValueError:
            self._logger.print(message=self.help_msg)
        except CalledProcessError:
            self._logger.print_and_log(self._prefix, ShellMsg.ERROR)
        return True
