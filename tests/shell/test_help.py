from typing import Any, Callable

import pytest
from pytest import CaptureFixture
from pytest_mock import MockFixture

LBA_RANGE = range(100)
HELP_MESSAGE = """Documented commands (type help <topic>):
  write\tWrite data to an LBA
  read\tRead data from an LBA
  fullwrite\tWrite data to all LBAs
  fullread\tRead data from all LBAs
  help\tShow help for commands"""

READ_HELP_MESSAGE = 'Invalid arguments. Usage: read <lba>'
WRITE_HELP_MESSAGE = 'Invalid arguments. Usage: write <lba> <hex data>'
MEMORY_MAP = {0: 0x00AABBCC, 1: 0x12345678, 99: 0x9ABCDEF0}

CommandHandler = Callable[[str], Any]


def help_message(*args, **kwargs) -> None:
    print(HELP_MESSAGE)


def parse_read_command(cmd: str) -> str:
    parts = cmd.split()
    if (
        len(parts) != 2
        or parts[0] != 'read'
        or not parts[1].isdigit()
        or int(parts[1]) not in LBA_RANGE
    ):
        raise ValueError(READ_HELP_MESSAGE)
    return parts[1]


def parse_write_command(cmd: str) -> tuple[str, str]:
    parts = cmd.split()
    if (
        len(parts) != 3
        or parts[0] != 'write'
        or not parts[1].isdigit()
        or int(parts[1]) not in LBA_RANGE
        or not (parts[2].startswith('0x') or parts[2].isdigit())
    ):
        raise ValueError(WRITE_HELP_MESSAGE)
    return parts[1], parts[2]


@pytest.fixture
def mock_shell(mocker: MockFixture) -> Any:
    mock_shell = mocker.Mock()
    mock_shell.cmd.side_effect = help_message
    return mock_shell


@pytest.fixture
def mock_file(mocker: MockFixture) -> Any:
    mock_file = mocker.Mock()
    mock_file.read.side_effect = lambda val: MEMORY_MAP[int(val)]
    mock_file.write.side_effect = lambda val: MEMORY_MAP[int(val[0])]
    return mock_file


def test_help_command_output(capsys: CaptureFixture, mock_shell) -> None:
    mock_shell.cmd.side_effect = help_message
    mock_shell.cmd('help')
    captured = capsys.readouterr()
    assert all(
        expected in captured.out
        for expected in ['write', 'read', 'fullwrite', 'fullread', 'help']
    )


def test_read_commands(mock_shell, mock_file) -> None:
    mock_shell.cmd.side_effect = lambda cmd: mock_file.read(parse_read_command(cmd))
    for call in mock_file.read.call_args_list:
        lba = call.args[0]
        assert MEMORY_MAP[int(lba)]


@pytest.mark.parametrize('command', ['read', 'read -1', 'read 100', 'read abc'])
def test_invalid_read_commands(command: str) -> None:
    with pytest.raises(ValueError, match=READ_HELP_MESSAGE):
        parse_read_command(command)


@pytest.mark.parametrize(
    'command',
    [
        'write 0 0xAABBCC',
        'write 1 0x12345678',
        'write 99 0x9ABCDEF0',
    ],
)
def test_write_commands(command: str, mock_shell, mock_file) -> None:
    mock_shell.cmd.side_effect = lambda cmd: mock_file.write(parse_write_command(cmd))
    for call in mock_file.write.call_args_list:
        mock_shell.cmd(command)
        lba, data = call.args[0]
        assert MEMORY_MAP[int(lba)] == int(data, 16)


@pytest.mark.parametrize(
    'command',
    [
        'write',
        'write 0',
        'write -1 0x123',
        'write 100 0x123',
        'write abc 0x123',
        'write 0 x123',
    ],
)
def test_invalid_write_commands(command: str) -> None:
    with pytest.raises(ValueError, match=WRITE_HELP_MESSAGE):
        parse_write_command(command)
