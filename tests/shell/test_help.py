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
