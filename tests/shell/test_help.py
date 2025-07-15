from typing import Any, Callable

import pytest
from pytest import CaptureFixture
from pytest_mock import MockFixture

from shell_constants import (
    LBA_RANGE,
    Hex,
)
from shell_constants import ShellCmd as Cmd
from shell_constants import ShellMsg as Msg

DUMMY_MEMORY_MAP = {0: 0x00AABBCC, 1: 0x12345678, 99: 0x9ABCDEF0}

CommandHandler = Callable[[str], Any]


def help_message(*args, **kwargs) -> None:
    print(Msg.HELP)


def parse_read_command(cmd: str) -> str:
    parts = cmd.split()
    if (
        len(parts) != 2
        or parts[0] != Cmd.READ
        or not parts[1].isdigit()
        or int(parts[1]) not in LBA_RANGE
    ):
        raise ValueError(Msg.READ_HELP)
    return parts[1]


def parse_write_command(cmd: str) -> tuple[str, str]:
    parts = cmd.split()
    if (
        len(parts) != 3
        or parts[0] != Cmd.WRITE
        or not parts[1].isdigit()
        or int(parts[1]) not in LBA_RANGE
        or not (parts[2].startswith(Hex.PREFIX) or parts[2].isdigit())
    ):
        raise ValueError(Msg.WRITE_HELP)
    return parts[1], parts[2]


@pytest.fixture
def mock_shell(mocker: MockFixture) -> Any:
    mock_shell = mocker.Mock()
    mock_shell.cmd.side_effect = help_message
    return mock_shell


@pytest.fixture
def mock_file(mocker: MockFixture) -> Any:
    mock_file = mocker.Mock()
    mock_file.read.side_effect = lambda val: DUMMY_MEMORY_MAP[int(val)]
    mock_file.write.side_effect = lambda val: DUMMY_MEMORY_MAP[int(val[0])]
    return mock_file


def test_help_command_output(capsys: CaptureFixture, mock_shell) -> None:
    mock_shell.cmd.side_effect = help_message
    mock_shell.cmd(Cmd.HELP)
    captured = capsys.readouterr()
    assert all(expected in captured.out for expected in Msg.HELP.split('\n'))


def test_read_commands(mock_shell, mock_file) -> None:
    mock_shell.cmd.side_effect = lambda cmd: mock_file.read(parse_read_command(cmd))
    for call in mock_file.read.call_args_list:
        lba = call.args[0]
        assert DUMMY_MEMORY_MAP[int(lba)]


@pytest.mark.parametrize(
    'command', [Cmd.READ, f'{Cmd.READ} -1', f'{Cmd.READ} 100', f'{Cmd.READ} abc']
)
def test_invalid_read_commands(command: str) -> None:
    with pytest.raises(ValueError, match=Msg.READ_HELP):
        parse_read_command(command)


@pytest.mark.parametrize(
    'command',
    [
        f'{Cmd.WRITE} 0 0x00AABBCC',
        f'{Cmd.WRITE} 1 0x12345678',
        f'{Cmd.WRITE} 99 0x9ABCDEF0',
    ],
)
def test_write_commands(command: str, mock_shell, mock_file) -> None:
    mock_shell.cmd.side_effect = lambda cmd: mock_file.write(parse_write_command(cmd))
    for call in mock_file.write.call_args_list:
        mock_shell.cmd(command)
        lba, data = call.args[0]
        assert DUMMY_MEMORY_MAP[int(lba)] == int(data, 16)


@pytest.mark.parametrize(
    'command',
    [
        Cmd.WRITE,
        f'{Cmd.WRITE} 0',
        f'{Cmd.WRITE} -1 0x123',
        f'{Cmd.WRITE} 100 0x123',
        f'{Cmd.WRITE} abc 0x123',
        f'{Cmd.WRITE} 0 x123',
    ],
)
def test_invalid_write_commands(command: str) -> None:
    with pytest.raises(ValueError, match=Msg.WRITE_HELP):
        parse_write_command(command)
