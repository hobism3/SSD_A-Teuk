from unittest.mock import patch

import pytest

from shell import Shell
from shell_constants import RUN_SSD
from shell_constants import ShellCmd as Cmd


@pytest.fixture
def mock_subprocess_run():
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ''
        mock_run.return_value.stderr = ''
        yield mock_run


@pytest.fixture
def shell(mock_subprocess_run):
    return Shell()


@pytest.fixture
def mock_commands():
    with (
        patch(
            'commands.write.WriteCommand.execute', return_value=True
        ) as execute_write,
        patch('commands.read.ReadCommand.execute', return_value=True) as execute_read,
        patch('commands.base.HelpCommand.execute', return_value=True) as execute_help,
        patch('commands.base.ExitCommand.execute', return_value=False) as execute_exit,
    ):
        yield {
            'write': execute_write,
            'read': execute_read,
            'help': execute_help,
            'exit': execute_exit,
        }


def run_shell_with_inputs(shell, inputs):
    with patch('builtins.input', side_effect=inputs):
        shell.run()


def assert_command_called_once(mock_commands, commands):
    for cmd in commands:
        mock_commands[cmd].assert_called_once()


@pytest.fixture
def user_inputs():
    return {
        'help_exit': [Cmd.HELP, Cmd.EXIT],
        'just_exit': [Cmd.EXIT],
        'write_then_exit': ['write 0 0x12345678', Cmd.EXIT],
        'read_then_exit': ['read 0', Cmd.EXIT],
        'empty_and_exit': ['', '  ', Cmd.EXIT],
        'unknown_then_exit': ['???', 'foo', 'blah', Cmd.EXIT],
        'keyboard_interrupt': KeyboardInterrupt(),
        'eof': EOFError(),
        'whitespace_and_case': ['  wRiTe 0 0x00ABCDEF  ', Cmd.EXIT],
        'exit_mid_loop': [Cmd.HELP, Cmd.EXIT, Cmd.HELP],
    }


@pytest.fixture
def expected_called():
    return {
        'help_exit': [Cmd.HELP, Cmd.EXIT],
        'just_exit': [Cmd.EXIT],
        'write_then_exit': [Cmd.WRITE, Cmd.EXIT],
        'read_then_exit': [Cmd.READ, Cmd.EXIT],
        'empty_and_exit': [Cmd.EXIT],
        'unknown_then_exit': [Cmd.EXIT],
        'keyboard_interrupt': [Cmd.EXIT],
        'eof': [Cmd.EXIT],
        'whitespace_and_case': [Cmd.EXIT],
        'exit_mid_loop': [Cmd.HELP, Cmd.EXIT],
    }


@pytest.fixture
def expected_subprocess_cmd():
    return {
        'write_then_exit': RUN_SSD + ['W', '0', '0x12345678'],
        'read_then_exit': RUN_SSD + ['R', '0'],
        'whitespace_and_case': RUN_SSD + ['W', '0', '0x00ABCDEF'],
    }
