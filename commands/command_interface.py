from typing import Protocol

from shell_tool.shell_logger import Logger


class CommandInterface(Protocol):
    _logger: Logger

    def execute(self, args: list[str] = None) -> bool: ...
