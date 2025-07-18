from unittest.mock import mock_open, patch

import pytest

from commands.meta import ExitCommand, HelpCommand
from commands.read import ReadCommand
from commands.write import WriteCommand
from shell import Shell
from shell_tool.shell_constants import RUN_SSD
from shell_tool.shell_constants import ShellMsg as Msg
from shell_tool.shell_constants import ShellPrefix as Pre
from shell_tool.shell_logger import Logger
from tests.shell.constants import *


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
def logger():
    return Logger()


@pytest.fixture
def mock_commands():
    with (
        patch(
            'commands.write.WriteCommand.execute', return_value=True
        ) as execute_write,
        patch('commands.read.ReadCommand.execute', return_value=True) as execute_read,
        patch('commands.meta.HelpCommand.execute', return_value=True) as execute_help,
        patch('commands.meta.ExitCommand.execute', return_value=False) as execute_exit,
    ):
        yield {
            'write': execute_write,
            'read': execute_read,
            'help': execute_help,
            'exit': execute_exit,
        }


def run_command_with_args(logger, command_cls, args, expected=''):
    with (
        patch('subprocess.run') as mock_run,
        patch('builtins.open', mock_open(read_data=expected)) as mock_file,
    ):
        cmd = command_cls(logger)
        result = cmd.execute(args)
    return mock_run, mock_file, result


def run_shell_with_inputs(shell, inputs):
    with patch('builtins.input', side_effect=inputs):
        shell.run()


def assert_command_called_once(mock_commands, commands):
    for cmd in commands:
        mock_commands[cmd].assert_called_once()


@pytest.fixture
def shell_user_inputs():
    return {
        SHELL_HELP_EXIT: [Cmd.HELP, Cmd.EXIT],
        SHELL_JUST_EXIT: [Cmd.EXIT],
        SHELL_WRITE_THEN_EXIT: [f'write {TEST_LBA} {TEST_DATA}', Cmd.EXIT],
        SHELL_READ_THEN_EXIT: [f'read {TEST_LBA}', Cmd.EXIT],
        SHELL_EMPTY_AND_EXIT: [TEST_EMPTY_OUTPUT, '  ', Cmd.EXIT],
        SHELL_UNKNOWN_THEN_EXIT: ['???', 'foo', 'blah', Cmd.EXIT],
        SHELL_KEYBOARD_INTERRUPT: KeyboardInterrupt(),
        SHELL_EOF: EOFError(),
        SHELL_WHITESPACE_AND_CASE: [f'  write {TEST_LBA} {TEST_DATA_2}  ', Cmd.EXIT],
        SHELL_EXIT_MID_LOOP: [Cmd.HELP, Cmd.EXIT, Cmd.HELP],
    }


@pytest.fixture
def shell_expected_called():
    return {
        SHELL_HELP_EXIT: [Cmd.HELP, Cmd.EXIT],
        SHELL_JUST_EXIT: [Cmd.EXIT],
        SHELL_WRITE_THEN_EXIT: [Cmd.WRITE, Cmd.EXIT],
        SHELL_READ_THEN_EXIT: [Cmd.READ, Cmd.EXIT],
        SHELL_EMPTY_AND_EXIT: [Cmd.EXIT],
        SHELL_UNKNOWN_THEN_EXIT: [Cmd.EXIT],
        SHELL_KEYBOARD_INTERRUPT: [Cmd.EXIT],
        SHELL_EOF: [Cmd.EXIT],
        SHELL_WHITESPACE_AND_CASE: [Cmd.EXIT],
        SHELL_EXIT_MID_LOOP: [Cmd.HELP, Cmd.EXIT],
    }


@pytest.fixture
def shell_expected_subprocess_cmd():
    return {
        SHELL_WRITE_THEN_EXIT: RUN_SSD + ['W', TEST_LBA, TEST_DATA],
        SHELL_READ_THEN_EXIT: RUN_SSD + ['R', TEST_LBA],
        SHELL_WHITESPACE_AND_CASE: RUN_SSD + ['W', TEST_LBA, TEST_DATA_2],
    }


@pytest.fixture
def cmd_input_args():
    return {
        CMD_WRITE: [WriteCommand, [TEST_LBA, TEST_DATA], TEST_EMPTY_OUTPUT],
        CMD_WRITE_INVALID: [WriteCommand, [TEST_LBA_INVALID, TEST_DATA], Msg.ERROR],
        CMD_READ: [ReadCommand, [TEST_LBA], TEST_READ_OUTPUT],
        CMD_READ_INVALID: [ReadCommand, [TEST_LBA_INVALID], Msg.ERROR],
        CMD_HELP: [HelpCommand, [], TEST_EMPTY_OUTPUT],
        CMD_EXIT: [ExitCommand, [], TEST_EMPTY_OUTPUT],
    }


@pytest.fixture
def cmd_expected_msg():
    return {
        CMD_WRITE: f'{Pre.WRITE} {Msg.DONE}',
        CMD_WRITE_INVALID: Msg.WRITE_HELP,
        CMD_READ: f'{Pre.READ} LBA {TEST_LBA:02}: {TEST_READ_OUTPUT}',
        CMD_READ_INVALID: Msg.READ_HELP,
        CMD_HELP: Msg.HELP,
        CMD_EXIT: TEST_EMPTY_OUTPUT,
    }
