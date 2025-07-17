from commands.erase import EraseCommand
from commands.read import ReadCommand
from commands.flush import FlushCommand
from shell_tool.shell_constants import ShellPrefix as Pre
from commands.write import WriteCommand
from shell_tool.shell_constants import RANGE_32BIT, MAX_LBA
import random

class CommandSupportMixin:
    def _get_command(self, attr_name, command_cls):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, command_cls(self._logger, prefix=None))
        return getattr(self, attr_name)

    def _run_command(self, command, args=None, quiet=False):
        args = args or []
        original_verbose = self._logger.verbose
        try:
            if quiet:
                self._logger.verbose = False
            command.execute(args)
        finally:
            self._logger.verbose = original_verbose
    
    def _parse_result(self, result):
        return ''

class WriteSupportMixin(CommandSupportMixin):
    @property
    def write_cmd(self) -> WriteCommand:
        return self._get_command('_write_cmd', WriteCommand)

    def write(self, lba, value, quiet=False):
        self._run_command(self.write_cmd, [str(lba), str(value)], quiet=quiet)

class WritePatternMixin(CommandSupportMixin):
    def write_random_n(self, lba: int, n: int, value_fn: callable = None):
        for _ in range(n):
            value = value_fn() if value_fn else self.rand32()
            self.write(lba, value)


class ReadSupportMixin(CommandSupportMixin):
    @property
    def read_cmd(self) -> ReadCommand:
        return self._get_command('_read_cmd', ReadCommand)

    def read(self, lba, quiet=False) -> str:
        self._run_command(self.read_cmd, [str(lba)], quiet=quiet)
        return self.read_cmd.result

    def read_with_verify(self, lba, expected, quiet=False) -> bool:
        read_value = self.read(lba, quiet=quiet)
        return read_value == expected


class EraseSupportMixin(CommandSupportMixin):
    @property
    def erase_cmd(self) -> EraseCommand:
        return self._get_command('_erase_cmd', EraseCommand)

    def erase(self, start_lba, size, quiet=False):
        if isinstance(start_lba, int):
            start_lba = str(start_lba)
        if isinstance(size, int):
            size = str(size)
        self._run_command(self.erase_cmd, [start_lba, size], quiet=quiet)
    
    def erase_range(self, start_lba, end_lba, quiet=False):
        if isinstance(start_lba, str):
            start_lba = int(start_lba)
        if isinstance(end_lba, str):
            end_lba = int(end_lba)
        size = end_lba - start_lba + 1
        self.erase(start_lba, size, quiet=quiet)


class FlushSupportMixin(CommandSupportMixin):
    @property
    def flush_cmd(self) -> FlushCommand:
        return self._get_command('_flush_cmd', FlushCommand)

    def flush(self, quiet=False):
        self._run_command(self.flush_cmd, quiet=quiet)

class RandomValueGenerateMixin:
    def rand32(self) -> str:
        return f'0x{random.getrandbits(32):08X}'
    
    def randvals(self, max_lba, step, unique=True) -> list[str]:
        num_chunks = (max_lba + step) // step

        if unique:
            if num_chunks > len(RANGE_32BIT):
                raise ValueError("Too many unique values requested.")
            values = random.sample(RANGE_32BIT, num_chunks)
        else:
            values = [random.choice(RANGE_32BIT) for _ in range(num_chunks)]

        return [f'0x{val:08X}' for val in values]