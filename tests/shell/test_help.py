import pytest
from pytest import CaptureFixture
from pytest_mock import MockFixture


def help_message(*args, **kwargs):
    print('Documented commands (type help <topic>):')
    print('  write\tWrite data to an LBA')
    print('  read\tRead data from an LBA')
    print('  fullwrite\tWrite data to all LBAs')
    print('  fullread\tRead data from all LBAs')
    print('  help\tShow help for commands')


def test_help_default(capsys: CaptureFixture, mocker: MockFixture) -> None:
    mock_shell = mocker.Mock()
    mock_shell.cmd.side_effect = lambda cmd: help_message() if cmd == 'help' else None
    mock_shell.cmd('help')
    captured = capsys.readouterr()
    output = captured.out

    assert 'Documented commands (type help <topic>):' in output
    assert 'write' in output
    assert 'read' in output
    assert 'fullwrite' in output
    assert 'fullread' in output
    assert 'help' in output


def parse_read_command(cmd: str) -> str:
    parts = cmd.split()
    if (
        len(parts) != 2
        or parts[0] != 'read'
        or not parts[1].isdigit()
        or not -1 < int(parts[1]) < 100
    ):
        raise ValueError('Invalid arguments. Usage: read <lba>')
    return parts[1]


def parse_write_command(cmd: str) -> tuple[str, str]:
    parts = cmd.split()
    if (
        len(parts) != 3
        or parts[0] != 'write'
        or not parts[1].isdigit()
        or not -1 < int(parts[1]) < 100
        or not (parts[2].startswith('0x') or parts[2].isdigit())
    ):
        raise ValueError('Invalid arguments. Usage: write <lba> <hex data>')
    return parts[1], parts[2]


def test_read_command_returns_expected_values_for_valid_inputs(
    mocker: MockFixture,
) -> None:
    expected_values = [0x00AABBCC, 0x12345678, 0x9ABCDEF0]
    mock_shell = mocker.Mock()
    mock_file = mocker.Mock()
    mock_file.read.side_effect = expected_values

    mock_shell.cmd.side_effect = lambda cmd: mock_file.read(parse_read_command(cmd))
    assert expected_values[0] == mock_shell.cmd('read 0')
    assert expected_values[1] == mock_shell.cmd('read 1')
    assert expected_values[2] == mock_shell.cmd('read 99')


def test_read_command_rejects_invalid_inputs(mocker: MockFixture) -> None:
    mock_shell = mocker.Mock()
    mock_shell.cmd.side_effect = lambda cmd: parse_read_command(cmd)

    with pytest.raises(ValueError, match='Invalid arguments. Usage: read <lba>'):
        mock_shell.cmd('read')  # Missing arguments
    with pytest.raises(ValueError, match='Invalid arguments. Usage: read <lba>'):
        mock_shell.cmd('read -1')  # LBA out of range
    with pytest.raises(ValueError, match='Invalid arguments. Usage: read <lba>'):
        mock_shell.cmd('read 100')  # LBA out of range
    with pytest.raises(ValueError, match='Invalid arguments. Usage: read <lba>'):
        mock_shell.cmd('read abc')  # Invalid LBA format


def test_write_command_returns_expected_values_for_valid_inputs(
    mocker: MockFixture,
) -> None:
    expected_responses = {0: 0x00AABBCC, 1: 0x12345678, 99: 0x9ABCDEF0}
    mock_shell = mocker.Mock()
    mock_file = mocker.Mock()
    mock_file.write.side_effect = lambda val: expected_responses[int(val[0])]
    mock_shell.cmd.side_effect = lambda cmd: mock_file.write(parse_write_command(cmd))
    mock_shell.cmd('write 0 0xAABBCC')
    mock_shell.cmd('write 1 0x12345678')
    mock_shell.cmd('write 99 0x9ABCDEF0')
    for call in mock_file.write.call_args_list:
        lba, data = call.args[0]
        assert expected_responses[int(lba)] == int(data, 16)


def test_write_command_rejects_invalid_inputs(mocker: MockFixture) -> None:
    mock_shell = mocker.Mock()
    mock_shell.cmd.side_effect = lambda cmd: parse_write_command(cmd)

    with pytest.raises(
        ValueError, match='Invalid arguments. Usage: write <lba> <hex data>'
    ):
        mock_shell.cmd('write')  # Missing arguments
    with pytest.raises(
        ValueError, match='Invalid arguments. Usage: write <lba> <hex data>'
    ):
        mock_shell.cmd('write 0')  # Missing data
    with pytest.raises(
        ValueError, match='Invalid arguments. Usage: write <lba> <hex data>'
    ):
        mock_shell.cmd('write -1 0x123')  # LBA out of range
    with pytest.raises(
        ValueError, match='Invalid arguments. Usage: write <lba> <hex data>'
    ):
        mock_shell.cmd('write 100 0x123')  # LBA out of range
    with pytest.raises(
        ValueError, match='Invalid arguments. Usage: write <lba> <hex data>'
    ):
        mock_shell.cmd('write abc 0x123')  # Invalid LBA format
    with pytest.raises(
        ValueError, match='Invalid arguments. Usage: write <lba> <hex data>'
    ):
        mock_shell.cmd('write 0 x123')  # Invalid data format
