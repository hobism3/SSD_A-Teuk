import pytest
from pytest_mock import MockerFixture

from shell import Shell


def test_shell_fullread(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()
    ssd.read.side_effect = ['0xFFFFFFFF' for _ in range(100)]

    mocker.patch('builtins.input', side_effect=['fullread', 'exit'])

    shell = Shell(ssd)
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Full Read]' in output
    for i in range(100):
        line = f'LBA {i:02d} : 0xFFFFFFFF'
        assert line in output


def test_shell_read_invalid_input(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()
    ssd.read.side_effect = [ValueError]

    mocker.patch('builtins.input', side_effect=['fullread 0 0', 'exit'])

    shell = Shell(ssd)
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Full Read] ERROR' in output


def test_shell_read_exception(capsys: pytest.CaptureFixture, mocker: MockerFixture):
    ssd = mocker.Mock()
    ssd.read.side_effect = [ValueError]

    mocker.patch('builtins.input', side_effect=['fullread', 'exit'])

    shell = Shell(ssd)
    shell.run()

    captured = capsys.readouterr()
    output = captured.out

    assert '[Full Read] ERROR' in output
